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
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect

red = [0xFF0000, 0xFF5555, 0x990000]
green = [0x00FF00, 0x55FF55, 0x009900]
dark = [0x0000FF, 0x5555FF, 0x000099]
light = [0x00FFFF, 0x55FFFF, 0x009999]
yellow = [0xFFFF00, 0xFFFF55, 0x999900]
purple = [0xFF00FF, 0xFF55FF, 0x990099]
orange = [0xFF7F00, 0xFFFF55, 0x992900]



# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=480, height=320)
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

def tetrisSign(x, y):
    #T
    time.sleep(0.5)
    tetrisBlock(x, y, red)
    tetrisBlock(x + 16, y, red)
    tetrisBlock(x + 16*2, y, red)
    tetrisBlock(x + 16, y + 16, red)
    tetrisBlock(x + 16, y + 16*2, red)
    tetrisBlock(x + 16, y + 16*3, red)
    tetrisBlock(x + 16, y + 16*4, red)
    #E
    time.sleep(0.5)
    tetrisBlock(x + 16*4, y, green)
    tetrisBlock(x + 16*5, y, green)
    tetrisBlock(x + 16*6, y, green)
    tetrisBlock(x + 16*4, y + 16, green)
    tetrisBlock(x + 16*4, y + 16*2, green)
    tetrisBlock(x + 16*5, y + 16*2, green)
    tetrisBlock(x + 16*4, y + 16, green)
    tetrisBlock(x + 16*4, y + 16*3, green)
    tetrisBlock(x + 16*4, y + 16*4, green)
    tetrisBlock(x + 16*5, y + 16*4, green)
    tetrisBlock(x + 16*6, y + 16*4, green)
    #T
    time.sleep(0.5)
    tetrisBlock(x + 16*8, y, dark)
    tetrisBlock(x + 16*9, y, dark)
    tetrisBlock(x + 16*10, y, dark)
    tetrisBlock(x + 16*9, y + 16, dark)
    tetrisBlock(x + 16*9, y + 16*2, dark)
    tetrisBlock(x + 16*9, y + 16*3, dark)
    tetrisBlock(x + 16*9, y + 16*4, dark)
    #R
    time.sleep(0.5)
    tetrisBlock(x + 16*12, y, red)
    tetrisBlock(x + 16*13, y, red)
    tetrisBlock(x + 16*14, y, red)
    tetrisBlock(x + 16*12, y + 16, red)
    tetrisBlock(x + 16*14, y + 16, red)
    tetrisBlock(x + 16*12, y + 16*2, red)
    tetrisBlock(x + 16*13, y + 16*2, red)
    tetrisBlock(x + 16*14, y + 16*2, red)
    tetrisBlock(x + 16*12, y + 16*3, red)
    tetrisBlock(x + 16*13, y + 16*3, red)
    tetrisBlock(x + 16*12, y + 16*4, red)
    tetrisBlock(x + 16*14, y + 16*4, red)
    #I
    time.sleep(0.5)
    tetrisBlock(x + 16*16, y, green)
    tetrisBlock(x + 16*17, y, green)
    tetrisBlock(x + 16*18, y, green)
    tetrisBlock(x + 16*17, y + 16, green)
    tetrisBlock(x + 16*17, y + 16*2, green)
    tetrisBlock(x + 16*17, y + 16*3, green)
    tetrisBlock(x + 16*16, y + 16*4, green)
    tetrisBlock(x + 16*17, y + 16*4, green)
    tetrisBlock(x + 16*18, y + 16*4, green)
    # S
    time.sleep(0.5)
    tetrisBlock(x + 16*20, y, dark)
    tetrisBlock(x + 16*21, y, dark)
    tetrisBlock(x + 16*22, y, dark)
    tetrisBlock(x + 16*20, y + 16, dark)
    tetrisBlock(x + 16*20, y + 16*2, dark)
    tetrisBlock(x + 16*21, y + 16*2, dark)
    tetrisBlock(x + 16*22, y + 16*2, dark)
    tetrisBlock(x + 16*22, y + 16*3, dark)
    tetrisBlock(x + 16*20, y + 16*4, dark)
    tetrisBlock(x + 16*21, y + 16*4, dark)
    tetrisBlock(x + 16*22, y + 16*4, dark)

    time.sleep(0.5)

old = [['b' for _ in range(20)] for _ in range(10)]

def newPiece():
	while len(splash) > 3:
		splash.pop()

def displayBoard(mat):
    for i in range(10):
        for j in range(20):
		    if(old[i][j] != mat[i][j]):
                old[i][j] = mat[i][j]
                if(mat[i][j] == 'r'):
                    tetrisBlock(i * 16 + 100, j * 16, red)
                if(mat[i][j] == 'g'):
                    tetrisBlock(i * 16 + 100, j * 16, green)
                if(mat[i][j] == 'd'):
                    tetrisBlock(i * 16 + 100, j * 16, dark)
                if(mat[i][j] == 'l'):
                    tetrisBlock(i * 16 + 100, j * 16, light)
                if(mat[i][j] == 'y'):
                    tetrisBlock(i * 16 + 100, j * 16, yellow)
                if(mat[i][j] == 'p'):
                    tetrisBlock(i * 16 + 100, j * 16, purple)
                if(mat[i][j] == 'o'):
                    tetrisBlock(i * 16 + 100, j * 16, orange)
                if(mat[i][j] == '0'):
                    splash.append(Rect(i * 16 + 100, j * 16, 16, 16, 0x000000))

def state1():
    while len(splash) > 0:
            splash.pop()
    background(0x091C3B)
    tetrisSign(20, 20)
    splash.append(RoundRect(10, 130, 300, 70, 5, fill=0xAA0088))
    splash.append(RoundRect(10, 230, 300, 70, 5, fill=0xAA0088))

    # Draw a label
    text_group = displayio.Group(scale=3, x=20, y=165)
    text = "Touch to start!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    text_group = displayio.Group(scale=3, x=60, y=265)
    text = "Leaderboard"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

def state2():
    pass

def state3():
    while len(splash) > 0:
        splash.pop()
    background(0x091C3B)
    splash.append(Rect(140, 20, 200, 70, outline=0xFFFFFF))
    splash.append(Rect(140, 90, 200, 210, outline=0xFFFFFF))

    # Draw a label
    text_group = displayio.Group(scale=2, x=170, y=55)
    text = "Leaderboard"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    text_group = displayio.Group(scale=2, x=160, y=125)
    text = "#1: 00300 ZAC"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    splash.append(RoundRect(370, 250, 80, 50, 5, outline=0xFFFFFF))

    text_group = displayio.Group(scale=2, x=380, y=275)
    text = "Back"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

#ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10)
ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10, calibration=((14810, 51555), (17403, 51095)), size=(480, 320))

state = 1

while True:
    print("Running")
    if (state == 1):
        print("Home")
        start = False
        state1()
        while (not start):
            p = ts.touch_point
            if p:
                x, y, pressure = p
                if(x > 170  and x < 470 and y > 130 and y < 200):
                    nextState = 2
                    start = True
                if(x > 170  and x < 470 and y > 230 and y < 300):
                    nextState = 3
                    start = True
                print("x= ", x)
                print("y= ", y)
        state = nextState
        

    if (state == 2):
        print("Game")
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
            matrix = [['0' for _ in range(20)] for _ in range(10)]
            matrix[0][i] = 'r'
            matrix[0][i + 1] = 'r'
            matrix[0][i + 2] = 'r'
            matrix[1][i + 2] = 'r'
            displayBoard(matrix)
            time.sleep(0.5)
        newPiece()

        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 100", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        for j in range(19):
            matrix = [['0' for _ in range(20)] for _ in range(10)]
            matrix[4][j] = 'g'
            matrix[4][j + 1] = 'g'
            matrix[5][j] = 'g'
            matrix[5][j + 1] = 'g'
            displayBoard(matrix)
            time.sleep(0.5)
        newPiece()


        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 200", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)

        for j in range(19):
            matrix = [['0' for _ in range(20)] for _ in range(10)]
            matrix[7][j] = 'd'
            matrix[8][j] = 'd'
            matrix[8][j + 1] = 'd'
            matrix[9][j + 1] = 'd'
            displayBoard(matrix)
            time.sleep(0.5)
        newPiece()


        splash.pop()
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: 300", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        splash.append(text_group)
        time.sleep(0.5)
        state = 3

    if (state == 3):
        print("Leaderboard")
        state3()
        start = False
        while (not start):
            p = ts.touch_point
            if p:
                x, y, pressure = p
                if(x > 30  and x < 110 and y > 250 and y < 300):
                    nextState = 1
                    start = True
                print("x= ", x)
                print("y= ", y)
        state = nextState
