# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import time
import board
import terminalio
import displayio
import adafruit_touchscreen
import adafruit_sdcard
from adafruit_display_text import label
from adafruit_display_shapes.polygon import Polygon
from adafruit_hx8357 import HX8357

red = [0xFF0000, 0xFF5555, 0x990000]
green = [0x00FF00, 0x55FF55, 0x009900]
blue = [0x0000FF, 0x5555FF, 0x000099]

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

display = HX8357(display_bus, width=480, height=320)

# Make the display context
splash = displayio.Group()
display.root_group = splash

def background(color):
    # Draw a bright green background
    while len(splash) > 0:
        splash.pop()
    color_bitmap = displayio.Bitmap(480, 320, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color
    splash.append(displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0))

def rectangle(x, y, length, width, color):
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(length, width, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = color
    splash.append(displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=x, y=y))

def tetrisBlock(x, y, color):
    inner_bitmap = displayio.Bitmap(16, 16, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = color[0]
    splash.append(displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=x, y=y))


    points = [(x, y), (x + 16, y), (x + 14, y + 2), (x + 2, y + 2)]  # Adjust for size and shape
    trapezoid = Polygon(points, outline=color[1])
    splash.append(trapezoid)
    points = [(x, y), (x, y + 16), (x + 2, y + 14), (x + 2, y + 2)]  # Adjust for size and shape
    trapezoid = Polygon(points, outline=color[1])
    splash.append(trapezoid)


    points = [(x + 16, y), (x + 16, y + 16), (x + 14, y + 14), (x + 14, y + 2)]  # Adjust for size and shape
    trapezoid = Polygon(points, outline=color[2])
    splash.append(trapezoid)
    points = [(x + 16, y + 16), (x, y + 16), (x + 2, y + 14), (x + 14, y + 14)]  # Adjust for size and shape
    trapezoid = Polygon(points, outline=color[2])
    splash.append(trapezoid)

def displayBoard(mat):
    for i in range(10):
        for j in range(20):
            if(mat[i][j] == 'r'):
                tetrisBlock(i * 16 + 100, j * 16, red)
            if(mat[i][j] == 'g'):
                tetrisBlock(i * 16 + 100, j * 16, green)
            if(mat[i][j] == 'd'):
                tetrisBlock(i * 16 + 100, j * 16, blue)

background(0x00FF00)
rectangle(90, 125, 300, 70, 0xAA0088)

# Draw a label
text_group = displayio.Group(scale=3, x=100, y=160)
text = "Touch to start!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

#ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10)
ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10, calibration=((14810, 51555), (17403, 51095)), size=(480, 320))

maxx = 0
maxy = 0
minx = 100000
miny = 100000
start = False

while True:
    time.sleep(0.1)
    if(start):
        print("Start")
        while len(splash) > 0:
            splash.pop()
        background(0x091C3B)

        rectangle(100, 0, 160, 320, 0x000000)

        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 0", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        for i in range(18):
            matrix = [['b' for _ in range(20)] for _ in range(10)]
            matrix[0][i] = 'r'
            matrix[0][i + 1] = 'r'
            matrix[0][i + 2] = 'r'
            matrix[1][i + 2] = 'r'
            displayBoard(matrix)
            time.sleep(0.5)
            while len(splash) > 3:
                splash.pop()

        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 100", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        for j in range(19):
            matrix = [['b' for _ in range(20)] for _ in range(10)]
            matrix[4][j] = 'g'
            matrix[4][j + 1] = 'g'
            matrix[5][j] = 'g'
            matrix[5][j + 1] = 'g'
            displayBoard(matrix)
            time.sleep(0.5)
            while len(splash) > 3:
                splash.pop()

        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 200", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        for j in range(19):
            matrix = [['b' for _ in range(20)] for _ in range(10)]
            matrix[7][j] = 'd'
            matrix[8][j] = 'd'
            matrix[8][j + 1] = 'd'
            matrix[9][j + 1] = 'd'
            displayBoard(matrix)
            time.sleep(0.5)
            while len(splash) > 3:
                splash.pop()

        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 300", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        while len(splash) > 0:
            splash.pop()
        background(0x00FF00)
        rectangle(90, 125, 300, 70, 0xAA0088)

        # Draw a label
        text_group = displayio.Group(scale=3, x=100, y=160)
        text = "HighScore: 300!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)

        while True:
            pass


    else:
        p = ts.touch_point
        if p:
            x, y, pressure = p
            start = x > 30 and x < 390 and y > 125 and y < 195
            maxx = max(maxx, x)
            maxy = max(maxy, y)
            minx = min(minx, x)
            miny = min(miny, y)
            print("x= ", minx, "x= ", maxx,)
            print("y= ", miny, "y= ", maxy,)
            print("x= ", x)
            print("y= ", y)
