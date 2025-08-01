import time
import board
import busio
import digitalio
import os

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess


class MonitorModule:
    def __init__(self):
        # Display Refresh
        self.LOOPTIME = 1.0

    def display_monitor(self, oled):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = oled.width
        height = oled.height
        image = Image.new('1', (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = height-padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Load default font.
        font = ImageFont.load_default()

        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # Icons website: https://icons8.com/line-awesome
        # Load fonts from the 'fonts' directory
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelOperator.ttf")
        icon_font_path = os.path.join(os.path.dirname(__file__), "fonts", "lineawesome-webfont.ttf")
        font = ImageFont.truetype(font_path, 18)
        icon_font = ImageFont.truetype(icon_font_path, 18)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
        IP = subprocess.check_output(cmd, shell = True )

        #cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
        #CPU = subprocess.check_output(cmd, shell = True )

        cmd = cmd = "mpstat 1 1 | awk '/Average/ {print 100 - $NF}'"
        CPU_Perc = subprocess.check_output(cmd, shell=True)

        # Decode and format
        cpu_str = "{:.1f}%".format(float(CPU_Perc.decode('utf-8').strip()))

        cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"    
        MemUsage = subprocess.check_output(cmd, shell = True )

        cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
        Disk = subprocess.check_output(cmd, shell = True )

        cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
        Temperature = subprocess.check_output(cmd, shell = True )

        # Icons 62609
        # Icon temperature
        draw.text((x, top+8),    chr(0xf2c7),  font=icon_font, fill=255)
        # Icon memory
        draw.text((x+65, top+8), chr(0xf538),  font=icon_font, fill=255)
        # Icon disk
        draw.text((x, top+28), chr(63426),  font=icon_font, fill=255)
        # Icon cpu
        draw.text((x, top+48), chr(62171), font=icon_font, fill=255)
        # Icon wifi
        #draw.text((x, top+48), chr(61931),  font=icon_font, fill=255)

        # Text
        # Text temperature
        draw.text((x+19, top+8), str(Temperature,'utf-8'),  font=font, fill=255)
        # Text memory usage
        draw.text((x+87, top+8), str(MemUsage,'utf-8'),  font=font, fill=255)
        # Text Disk usage
        draw.text((x+19, top+28), str(Disk,'utf-8'),  font=font, fill=255)
        # Text cpu usage
        draw.text((x+19, top+48), cpu_str, font=font, fill=255)
        # Text IP address
        #draw.text((x+19, top+48), str(IP,'utf-8'),  font=font, fill=255)

        # Display image.
        oled.image(image)
        oled.show()
        time.sleep(self.LOOPTIME)
