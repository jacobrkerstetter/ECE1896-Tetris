import board
import time
import terminalio
import displayio
import adafruit_touchscreen
from adafruit_display_text import label
from adafruit_display_shapes.polygon import Polygon
from adafruit_hx8357 import HX8357
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
import gc
from algorithm.game import *

displayio.release_displays()
#Setup touchreen pins
#ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10)
ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10, calibration=((10500, 53000), (16000, 44800)), size=(480, 320))

#Connect teensy SPI for display communcation
spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=480, height=320)
#Create Display splash
splash = displayio.Group()
display.root_group = splash


touch_label = label.Label(terminalio.FONT, text="Touch: ", color=0xFFFFFF, x=10, y=10)
splash.append(touch_label)

# Main loop to test touchscreen
print("Touchscreen test started. Touch the screen to see coordinates.")
while True:
    # Check for touch events
    touch = ts.touch_point
    if touch:
        # Update label with touch coordinates
        x, y, pressure = touch
        touch_label.text = f"Touch: X={x}, Y={y}, P={pressure}"
        print(f"Touch detected: X={x}, Y={y}, Pressure={pressure}")
    else:
        # Clear the label if no touch is detected
        touch_label.text = "Touch: None"

    # Delay to avoid flooding the console
    time.sleep(0.1)
