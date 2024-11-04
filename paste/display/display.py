import board
import time
import terminalio
import displayio
import adafruit_touchscreen
import adafruit_sdcard
from adafruit_display_text import label
from adafruit_display_shapes.polygon import Polygon
from adafruit_hx8357 import HX8357
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect
import gc
from algorithm.game import *

"""
Dsiplay uses 5v and GND

SPI MODE
TEENSY  ->  ADAFRUIT_SPI

Display
D9      ->  CS 
D10     ->  D/C
D11     ->  MOSI
D12     ->  RST
D13     ->  CLOCK
Touchscreen
D24     ->  Y+
D25     ->  X+
D26     ->  Y-
D27     ->  X-

"""

class Display():
    def __init__(self):
    #Color arrays for tetris square [Main, Lighter, Darker]
        self.red = [0xFF0000, 0xFF5555, 0x990000]
        self.green = [0x00FF00, 0x55FF55, 0x009900]
        self.dark = [0x0000FF, 0x5555FF, 0x000099]
        self.light = [0x00FFFF, 0x55FFFF, 0x009999]
        self.yellow = [0xFFFF00, 0xFFFF55, 0x999900]
        self.purple = [0xFF00FF, 0xFF55FF, 0x990099]
        self.orange = [0xFF7F00, 0xFFFF55, 0x992900]

        # Release any resources currently in use for the displays
        displayio.release_displays()
        #Setup touchreen pins
        self.ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10, calibration=((14810, 51555), (17403, 51095)), size=(480, 320))

        #Connect teensy SPI for display communcation
        spi = board.SPI()
        tft_cs = board.D9
        tft_dc = board.D10
        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = HX8357(display_bus, width=480, height=320)
        #Create Display splash
        self.splash = displayio.Group()
        self.display.root_group = self.splash

        #Matrices to hold the old color and the previous pieces
        self.old = [['0' for _ in range(10)] for _ in range(20)]
        self.prev = [[0 for _ in range(10)] for _ in range(20)]

        self.currScore = 0

        self.highlight = 0

        self.prevPiece = 0
        self.prevPieceSplash = 0

    #Function to color entire background
    def background(self, color):
        while len(self.splash) > 0:
            self.splash.pop()
        color_bitmap = displayio.Bitmap(480, 320, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = color
        self.splash.append(displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0))

    #Create a tetris block given coordinates and color array and return array of splash
    def tetrisBlock(self, x, y, color):
        #Create square using main color
        square = Rect(x,y,16,16, fill=color[0])
        self.splash.append(square)

        #Create top and left trapezoid using light color
        points = [(x, y), (x + 15, y), (x + 13, y + 2), (x + 2, y + 2)]
        trapezoid1 = Polygon(points, outline=color[1])
        self.splash.append(trapezoid1)
        points = [(x, y), (x, y + 15), (x + 2, y + 13), (x + 2, y + 2)]
        trapezoid2 = Polygon(points, outline=color[1])
        self.splash.append(trapezoid2)

        #Create bottom and right trapezoid using dark color
        points = [(x + 15, y), (x + 15, y + 15), (x + 13, y + 13), (x + 13, y + 2)]
        trapezoid3 = Polygon(points, outline=color[2])
        self.splash.append(trapezoid3)
        points = [(x + 15, y + 15), (x, y + 15), (x + 2, y + 13), (x + 13, y + 13)]
        trapezoid4 = Polygon(points, outline=color[2])
        self.splash.append(trapezoid4)

        #Return Splash elements for further use
        return [square, trapezoid1, trapezoid2, trapezoid3, trapezoid4]

#Create tetris sign using tetris block function
    def tetrisSign(self, x, y):
        #T
        time.sleep(0.3)
        color = self.purple
        self.tetrisBlock(x, y, color)
        self.tetrisBlock(x + 16, y, color)
        self.tetrisBlock(x + 16*2, y, color)
        self.tetrisBlock(x + 16, y + 16, color)
        self.tetrisBlock(x + 16, y + 16*2, color)
        self.tetrisBlock(x + 16, y + 16*3, color)
        self.tetrisBlock(x + 16, y + 16*4, color)
        #E
        time.sleep(0.3)
        color = self.red
        self.tetrisBlock(x + 16*4, y, color)
        self.tetrisBlock(x + 16*5, y, color)
        self.tetrisBlock(x + 16*6, y, color)
        self.tetrisBlock(x + 16*4, y + 16, color)
        self.tetrisBlock(x + 16*4, y + 16*2, color)
        self.tetrisBlock(x + 16*5, y + 16*2, color)
        self.tetrisBlock(x + 16*4, y + 16, color)
        self.tetrisBlock(x + 16*4, y + 16*3, color)
        self.tetrisBlock(x + 16*4, y + 16*4, color)
        self.tetrisBlock(x + 16*5, y + 16*4, color)
        self.tetrisBlock(x + 16*6, y + 16*4, color)
        #T
        time.sleep(0.3)
        color = self.dark
        self.tetrisBlock(x + 16*8, y, color)
        self.tetrisBlock(x + 16*9, y, color)
        self.tetrisBlock(x + 16*10, y, color)
        self.tetrisBlock(x + 16*9, y + 16, color)
        self.tetrisBlock(x + 16*9, y + 16*2, color)
        self.tetrisBlock(x + 16*9, y + 16*3, color)
        self.tetrisBlock(x + 16*9, y + 16*4, color)
        #R
        time.sleep(0.3)
        color = self.green
        self.tetrisBlock(x + 16*12, y, color)
        self.tetrisBlock(x + 16*13, y, color)
        self.tetrisBlock(x + 16*12, y + 16, color)
        self.tetrisBlock(x + 16*14, y + 16, color)
        self.tetrisBlock(x + 16*12, y + 16*2, color)
        self.tetrisBlock(x + 16*13, y + 16*2, color)
        self.tetrisBlock(x + 16*14, y + 16*2, color)
        self.tetrisBlock(x + 16*12, y + 16*3, color)
        self.tetrisBlock(x + 16*13, y + 16*3, color)
        self.tetrisBlock(x + 16*12, y + 16*4, color)
        self.tetrisBlock(x + 16*14, y + 16*4, color)
        #I
        time.sleep(0.3)
        color = self.light
        self.tetrisBlock(x + 16*16, y, color)
        self.tetrisBlock(x + 16*17, y, color)
        self.tetrisBlock(x + 16*18, y, color)
        self.tetrisBlock(x + 16*17, y + 16, color)
        self.tetrisBlock(x + 16*17, y + 16*2, color)
        self.tetrisBlock(x + 16*17, y + 16*3, color)
        self.tetrisBlock(x + 16*16, y + 16*4, color)
        self.tetrisBlock(x + 16*17, y + 16*4, color)
        self.tetrisBlock(x + 16*18, y + 16*4, color)
        # S
        time.sleep(0.3)
        color = self.orange
        self.tetrisBlock(x + 16*20, y, color)
        self.tetrisBlock(x + 16*21, y, color)
        self.tetrisBlock(x + 16*22, y, color)
        self.tetrisBlock(x + 16*20, y + 16, color)
        self.tetrisBlock(x + 16*20, y + 16*2, color)
        self.tetrisBlock(x + 16*21, y + 16*2, color)
        self.tetrisBlock(x + 16*22, y + 16*2, color)
        self.tetrisBlock(x + 16*22, y + 16*3, color)
        self.tetrisBlock(x + 16*20, y + 16*4, color)
        self.tetrisBlock(x + 16*21, y + 16*4, color)
        self.tetrisBlock(x + 16*22, y + 16*4, color)

        time.sleep(0.3)

    #Function to pop an index array
    def popOne(self, pops):
        for part in pops:
            self.splash.remove(part)


    def scoreUpdate(self, score):
        self.splash.remove(self.currScore)
        #Create score counter
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: " + str(score), color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.currScore = text_group
        self.splash.append(text_group)

    def displayNext(self, nextPiece):
        if(self.prevPiece != nextPiece):
            self.prevPiece = nextPiece
            for part in self.prevPieceSplash:
                    self.splash.remove(part)
            if(isinstance(nextPiece,JBlock)):
                self.prevPieceSplash = self.tetrisBlock(300, 80 ,self.light)
                self.prevPieceSplash.append = self.tetrisBlock(300, 96 ,self.light)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.light)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.light)
            if(isinstance(nextPiece,LBlock)):
                self.prevPieceSplash = self.tetrisBlock(300, 96 ,self.orange)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.orange)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.orange)
                self.prevPieceSplash.append = self.tetrisBlock(332, 80 ,self.orange)
            if(isinstance(nextPiece,IBlock)):
                self.prevPieceSplash = self.tetrisBlock(300, 96 ,self.dark)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.dark)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.dark)
                self.prevPieceSplash.append = self.tetrisBlock(348, 96 ,self.dark)
            if(isinstance(nextPiece,SBlock)):
                self.prevPieceSplash = self.tetrisBlock(316, 80 ,self.green)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.green)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.green)
                self.prevPieceSplash.append = self.tetrisBlock(332, 112 ,self.green)
            if(isinstance(nextPiece,TBlock)):
                self.prevPieceSplash = self.tetrisBlock(316, 80 ,self.purple)
                self.prevPieceSplash.append = self.tetrisBlock(300, 96 ,self.purple)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.purple)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.purple)
            if(isinstance(nextPiece,ZBlock)):
                self.prevPieceSplash = self.tetrisBlock(300, 112 ,self.red)
                self.prevPieceSplash.append = self.tetrisBlock(300, 96 ,self.red)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.red)
                self.prevPieceSplash.append = self.tetrisBlock(316, 80 ,self.red)
            if(isinstance(nextPiece,OBlock)):
                self.prevPieceSplash = self.tetrisBlock(316, 80 ,self.yellow)
                self.prevPieceSplash.append = self.tetrisBlock(316, 96 ,self.yellow)
                self.prevPieceSplash.append = self.tetrisBlock(332, 80 ,self.yellow)
                self.prevPieceSplash.append = self.tetrisBlock(332, 96 ,self.yellow)



    #Function to take game array and draw and remove blocks as they fall or are cleared
    def displayBoard(self, mat, nextPiece):
        self.displayNext(nextPiece)

        for i in range(10):
            for j in range(20):
                #If there is a difference
                if self.old[j][i] != mat[j][i]:
                    if mat[j][i] == "r":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.red)
                    if mat[j][i] == "g":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.green)
                    if mat[j][i] == "d":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.dark)
                    if mat[j][i] == "l":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.light)
                    if mat[j][i] == "y":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.yellow)
                    if mat[j][i] == "p":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.purple)
                    if mat[j][i] == "o":
                        self.prev[j][i] = self.tetrisBlock(i * 16 + 100, j * 16, self.orange)
                    if mat[j][i] == "0":
                        self.popOne(self.prev[j][i])
                        # hold = Rect(i * 16 + 100, j * 16, 16, 16, fill=0x000000, outline = 0x000000)
                        # splash.append(hold)
                    self.old[j][i] = mat[j][i]

    #Home screen state
    def state1(self):
        #Clear entire board
        while len(self.splash) > 0:
                self.splash.pop()
        # self.display.root_group = None
        # gc.collect()
        # self.splash = displayio.Group()
        # self.display.root_group = self.splash

        #Setup background and tetris sign
        self.background(0x091C3B)
        self.tetrisSign(20, 20)

        #Create Start button
        self.splash.append(RoundRect(10, 120, 300, 50, 5, fill=0xAA0088))
        text_group = displayio.Group(scale=3, x=20, y=145)
        text = "Touch to start!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)

        #Create Help Button
        self.splash.append(RoundRect(10, 190, 300, 50, 5, fill=0xAA0088))
        text_group = displayio.Group(scale=3, x=110, y=215)
        text = "Help"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)

        #Create Leaderboard button
        self.splash.append(RoundRect(10, 260, 300, 50, 5, fill=0xAA0088))
        text_group = displayio.Group(scale=3, x=60, y=285)
        text = "Leaderboard"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)

        #Loop to start searching for touch inputs for next state
        self.highlight = RoundRect(10, 120, 300, 50, 5, outline = 0xFFFF00)
        self.splash.append(self.highlight)

        start = False
        while (not start):
                p = self.ts.touch_point
                if p:
                    x, y, pressure = p
                    if(x > 160  and x < 480 and y > 110 and y < 180):
                        nextState = 2
                        self.homeOutline(nextState)
                        start = True
                        
                    if(x > 160  and x < 480 and y > 180 and y < 250):
                        nextState = 5
                        self.homeOutline(nextState)
                        start = True
                        
                    if(x > 160  and x < 480 and y > 250 and y < 320):
                        nextState = 3
                        self.homeOutline(nextState)
                        start = True
                        
                    print("x= ", x)
                    print("y= ", y)

        return nextState
    
    def homeOutline(self, i):
        self.splash.remove(self.highlight)
        if(i == 2):
            self.highlight = RoundRect(10, 120, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)
        elif(i == 4):
            self.highlight = RoundRect(10, 190, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)
        else:
            self.highlight = RoundRect(10, 260, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)

    def state2(self):
        #Clear board
        while len(self.splash) > 0:
                self.splash.pop()
        
        #Set background and gameboard
        self.background(0x091C3B)
        self.splash.append(Rect(100,0,160,320, fill=0x000000))

        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: " + str(0), color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.currScore = text_group
        self.splash.append(text_group)

        text_group = displayio.Group(scale=2, x=300, y=50)
        text_area = label.Label(terminalio.FONT, text="Next Piece:", color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.currScore = text_group
        self.splash.append(text_group)

        self.splash.append(Rect(300,80,64,48, fill=0x000000, outline=0xFFFFFF))



    

    def state3(self):
        #Clear board
        while len(self.splash) > 0:
            self.splash.pop()
        self.background(0x091C3B)
        
        #Create leaderboard board
        self.splash.append(Rect(140, 20, 200, 70, outline=0xFFFFFF))
        self.splash.append(Rect(140, 90, 200, 210, outline=0xFFFFFF))
        text_group = displayio.Group(scale=2, x=170, y=55)
        text = "Leaderboard"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)
        self.splash.append(text_group)
        
        #Display list of top 10 scores
        for i in range (10):
            text_group = displayio.Group(scale=1, x=160, y=120 + i * 15)
            score = 0
            tag = "Zac"
            text = "#" + str(i) + " " + str(score) + " " + tag
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
            text_group.append(text_area)  # Subgroup for text scaling
            self.splash.append(text_group)

        #Create Back button
        self.splash.append(RoundRect(370, 250, 80, 50, 5, outline=0xFFFFFF))
        text_group = displayio.Group(scale=2, x=380, y=275)
        text = "Back"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)

        #Loop for touchscreen of back button
        start = False
        while (not start):
            p = self.ts.touch_point
            if p:
                x, y, pressure = p
                if(x > 20  and x < 120 and y > 240 and y < 310):
                    nextState = 1
                    start = True
                print("x= ", x)
                print("y= ", y)
            
        return nextState
    

    def state4(self):
        while len(self.splash) > 0:
            self.splash.pop()
        return 1
    
    def state5(self):
        while len(self.splash) > 0:
            self.splash.pop()
        self.background(0x091C3B)
        layout = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
        for i in range(10):
            self.splash.append(RoundRect(i * 35 + 70, 100, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 75, y=112)
            text_group.append(label.Label(terminalio.FONT, text=layout[i], color=0xFFFFFF))  # Subgroup for text scaling
            self.splash.append(text_group)

        layout = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
        for i in range(9):
            self.splash.append(RoundRect(i * 35 + 87, 170, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 92, y=182)
            text_group.append(label.Label(terminalio.FONT, text=layout[i], color=0xFFFFFF))  # Subgroup for text scaling
            self.splash.append(text_group)

        layout = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ']
        for i in range(8):
            self.splash.append(RoundRect(i * 35 + 105, 240, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 111, y=252)
            text_group.append(label.Label(terminalio.FONT, text=layout[i], color=0xFFFFFF))  # Subgroup for text scaling
            self.splash.append(text_group)

        self.splash.append(Rect( 188, 80, 25, 3, fill=0xFFFFFF))
        self.splash.append(Rect( 228, 80, 25, 3, fill=0xFFFFFF))
        self.splash.append(Rect( 268, 80, 25, 3, fill=0xFFFFFF))
        time.sleep(5)

        return 1
    