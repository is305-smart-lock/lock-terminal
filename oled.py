import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import ImageDraw, ImageFont, Image

# Raspberry Pi pin configuration:
RST = 17
# Note the following are only used with SPI:
DC = 27
SPI_PORT = 0
SPI_DEVICE = 0

def render(text = None):
    # 128x64 display with hardware SPI:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 1
    top = padding
    x = padding
    # Load default font.

    # Alternatively load a TTF font.
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('Minecraftia.ttf', 8)

    if text != None:
        for index, value in enumerate(text):
            # Write two lines of text.
            font = ImageFont.truetype('MSYH.TTC', value['size'])
            draw.text((x, top + 20 * index), value['text'], font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
