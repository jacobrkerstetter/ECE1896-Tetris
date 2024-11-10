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
from adafruit_display_shapes.line import Line
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
    #Private variable creation
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
        self.ts = adafruit_touchscreen.Touchscreen(board.A13, board.A11, board.D26, board.A10, calibration=((10500, 53000), (16000, 44800)), size=(480, 320))

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

        #Hold for current game score splash
        self.currScore = None
        self.heldScore = None

        #Hold for current highlight
        self.highlight = None

        #Holds for previous piece and previous piece splash
        self.prevPiece = None
        self.prevPieceSplash = None

        #Holds for highlight index
        self.xindex = None
        self.yindex = None
        self.count = None
        #Hold for keyboard layout
        self.layout = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'], ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'], ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '-']]
        self.character = ['Z','A','C']

    #Function to color entire background
    def background(self, color):
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

    def tetrisBlockParts(self, x, y, color):
        #Create square using main color
        square = Rect(x,y,16,16, fill=color[0])

        #Create top and left trapezoid using light color
        points = [(x, y), (x + 15, y), (x + 13, y + 2), (x + 2, y + 2)]
        trapezoid1 = Polygon(points, outline=color[1])
        points = [(x, y), (x, y + 15), (x + 2, y + 13), (x + 2, y + 2)]
        trapezoid2 = Polygon(points, outline=color[1])

        #Create bottom and right trapezoid using dark color
        points = [(x + 15, y), (x + 15, y + 15), (x + 13, y + 13), (x + 13, y + 2)]
        trapezoid3 = Polygon(points, outline=color[2])
        points = [(x + 15, y + 15), (x, y + 15), (x + 2, y + 13), (x + 13, y + 13)]
        trapezoid4 = Polygon(points, outline=color[2])
        
        #Create Displayio group 
        group = displayio.Group()
        group.append(square)
        group.append(trapezoid1)
        group.append(trapezoid2)
        group.append(trapezoid3)
        group.append(trapezoid4)

        #Return Splash elements for further use
        return group

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

    #Function to pop an index array
    def popOne(self, pops):
        for part in pops:
            self.splash.remove(part)

    #Function that recives score and updates the current score
    def scoreUpdate(self, score):
        self.heldScore = score
        #Remove previous score
        self.splash.remove(self.currScore)
        #Create score counter
        text_group = displayio.Group(scale=2, x=300, y=20)
        text_area = label.Label(terminalio.FONT, text="Score: " + str(score), color=0xFFFFFF)
        text_group.append(text_area)
        self.currScore = text_group
        self.splash.append(text_group)

    #Function that dsplays the upcoming tetris piece
    def displayNext(self, nextPiece):
        #Remove the previous next if there is a difference
        if(self.prevPiece != nextPiece):
            if self.prevPieceSplash is not None:
                self.popOne(self.prevPieceSplash)
            self.prevPiece = nextPiece
            #Display a default J block
            self.prevPieceSplash = []
            if(isinstance(nextPiece,JBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 80 + 8 ,self.light))
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 96 + 8 ,self.light))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 96 + 8 ,self.light))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 96 + 8 ,self.light))
            #Display a default L block
            if(isinstance(nextPiece,LBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 96 + 8 ,self.orange))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 96 + 8 ,self.orange))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 96 + 8 ,self.orange))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 80 + 8 ,self.orange))
            #Display a default I block
            if(isinstance(nextPiece,IBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(300, 96 ,self.dark))
                self.prevPieceSplash.append(self.tetrisBlockParts(316, 96 ,self.dark))
                self.prevPieceSplash.append(self.tetrisBlockParts(332, 96 ,self.dark))
                self.prevPieceSplash.append(self.tetrisBlockParts(348, 96 ,self.dark))
            #Display a default S block
            if(isinstance(nextPiece,SBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 96 + 8 ,self.green))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 96 + 8 ,self.green))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 80 + 8 ,self.green))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 80 + 8 ,self.green))
            #Display a default T block
            if(isinstance(nextPiece,TBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 80 + 8 ,self.purple))
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 96 + 8 ,self.purple))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 96 + 8 ,self.purple))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 96 + 8 ,self.purple))
            #Dsiplay a default Z block
            if(isinstance(nextPiece,ZBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(300 + 8, 80 + 8 ,self.red))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 80 + 8 ,self.red))
                self.prevPieceSplash.append(self.tetrisBlockParts(316 + 8, 96 + 8 ,self.red))
                self.prevPieceSplash.append(self.tetrisBlockParts(332 + 8, 96 + 8 ,self.red))
            #Display a default O block
            if(isinstance(nextPiece,OBlock)):
                self.prevPieceSplash.append(self.tetrisBlockParts(316, 80 + 8 ,self.yellow))
                self.prevPieceSplash.append(self.tetrisBlockParts(316, 96 + 8 ,self.yellow))
                self.prevPieceSplash.append(self.tetrisBlockParts(332, 80 + 8 ,self.yellow))
                self.prevPieceSplash.append(self.tetrisBlockParts(332, 96 + 8 ,self.yellow))
            for part in self.prevPieceSplash:
                self.splash.append(part)


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
                    self.old[j][i] = mat[j][i]
        gc.collect()

    #Home screen state
    def state1(self):
        self.__init__
        print(f"Free memory: {gc.mem_free()} bytes")
        #Clear entire board
        self.old = [['0' for _ in range(10)] for _ in range(20)]
        self.prevPieceSplash = None
        print(f"Free memory: {gc.mem_free()} bytes")
        while len(self.splash) > 0:
                self.splash.pop()
        self.clearMem()
        print(f"Free memory: {gc.mem_free()} bytes")

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

        self.xindex = 0
        self.yindex = 0

    def state2(self):
        print(f"Free memory: {gc.mem_free()} bytes")
        #Clear board
        while len(self.splash) > 0:
                self.splash.pop()
        self.clearMem()

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
        self.splash.append(text_group)

        self.splash.append(Rect(299,79,66,50, fill=0x000000, outline=0xFFFFFF))

        self.prev = [[0 for _ in range(10)] for _ in range(20)]

    def gameOver(self):
        self.prevPiece = None
        self.prevPieceSplash = None
        self.prev = None
        while len(self.splash) > 0:
                self.splash.pop()
        self.clearMem()

        self.background(0x091C3B)

        text_group = displayio.Group(scale=4, x=100, y=50)
        text_area = label.Label(terminalio.FONT, text="GAME OVER!", color=0xFFFFFF)
        text_group.append(text_area)
        self.splash.append(text_group)

        text_group = displayio.Group(scale=3, x=100, y=200)
        text = "Final Score: " + str(self.heldScore)
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)
        self.splash.append(text_group)
        time.sleep(2)


    def state3(self):
        self.highlight = None
        print(f"Free memory: {gc.mem_free()} bytes")
        #Clear board
        while len(self.splash) > 0:
            self.splash.pop()
        self.clearMem()
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
            tag = str(self.character[0] + self.character[1] + self.character[2])
            text = "#" + str(i+1) + " " + str(self.heldScore) + " " + tag
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
            text_group.append(text_area)  # Subgroup for text scaling
            self.splash.append(text_group)
            time.sleep(0.1)

        #Create Back button
        self.splash.append(RoundRect(370, 250, 80, 50, 5, outline=0xFFFFFF))
        text_group = displayio.Group(scale=2, x=380, y=275)
        text = "Back"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.splash.append(text_group)
    

    def state4(self):
        print(f"Free memory: {gc.mem_free()} bytes")
        while len(self.splash) > 0:
            self.splash.pop()
        self.clearMem()

        self.background(0x091C3B)

        #Left
        self.splash.append(Circle(100, 160, 20, outline=0x000000, fill=0xFF0000))
        triangle_points = [(100 + 5, 160 + 15), (100 + 5, 160 - 15), (100 - 10, 160)]
        triangle = Polygon(points=triangle_points, outline=0x000000)
        self.splash.append(triangle)
        time.sleep(0.1)
        #Right
        self.splash.append(Circle(170, 160, 20, outline=0x000000, fill=0xFF0000))
        triangle_points = [(170 - 5, 160 - 15), (170 - 5, 160 + 15), (170 + 10, 160)]
        triangle = Polygon(points=triangle_points, outline=0x000000)
        self.splash.append(triangle)
        time.sleep(0.1)
        #Up
        self.splash.append(Circle(135, 125, 20, outline=0x000000, fill=0xFF0000))
        triangle_points = [(135 - 15, 125 + 5), (135 + 15, 125 + 5), (135, 125 - 10)]
        triangle = Polygon(points=triangle_points, outline=0x000000)
        self.splash.append(triangle)
        time.sleep(0.1)
        #Down
        self.splash.append(Circle(135, 195, 20, outline=0x000000, fill=0xFF0000))
        triangle_points = [(135 + 15, 195 - 5), (135 - 15, 195 - 5), (135, 195 + 10)]
        triangle = Polygon(points=triangle_points, outline=0x000000)
        self.splash.append(triangle)
        time.sleep(0.1)

        #A
        self.splash.append(Circle(310, 177, 20, outline=0x000000, fill=0xFF0000))
        text_group = displayio.Group(scale=3, x=305, y=177)
        text_area = label.Label(terminalio.FONT, text='A', color=0x000000)
        text_group.append(text_area)
        self.splash.append(text_group)
        time.sleep(0.1)
        
        #B
        self.splash.append(Circle(345, 143, 20, outline=0x000000, fill=0xFF0000))
        text_group = displayio.Group(scale=3, x=340, y=143)
        text_area = label.Label(terminalio.FONT, text='B', color=0x000000)
        text_group.append(text_area)
        self.splash.append(text_group)
        time.sleep(0.1)

        self.splash.append(Line(100, 180, 100, 250, color=0xFFFFFF))
        self.splash.append(Line(170, 180, 170, 250, color=0xFFFFFF))
        self.splash.append(Line(135, 215, 135, 250, color=0xFFFFFF))
        self.splash.append(Line(100, 250, 170, 250, color=0xFFFFFF))
        
        text_group = displayio.Group(scale=1, x=60, y=260)
        text_area = label.Label(terminalio.FONT, text="Controls block movement:", color=0xFFFFFF)
        text_group.append(text_area)
        self.splash.append(text_group)
        text_group = displayio.Group(scale=1, x=65, y=280)
        text_area = label.Label(terminalio.FONT, text="left, right, and down", color=0xFFFFFF)
        text_group.append(text_area)
        self.splash.append(text_group)

        
        
        time.sleep(5)
        return 1
    
    def state5(self):
        print(f"Free memory: {gc.mem_free()} bytes")
        while len(self.splash) > 0:
            self.splash.pop()
        self.clearMem()
        self.background(0x091C3B)
        for i in range(10):
            self.splash.append(RoundRect(i * 35 + 70, 100, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 75, y=112)
            text_group.append(label.Label(terminalio.FONT, text=self.layout[0][i], color=0xFFFFFF))
            self.splash.append(text_group)
            time.sleep(0.1)

        for i in range(9):
            self.splash.append(RoundRect(i * 35 + 87, 170, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 92, y=182)
            text_group.append(label.Label(terminalio.FONT, text=self.layout[1][i], color=0xFFFFFF))
            self.splash.append(text_group)
            time.sleep(0.1)

        for i in range(8):
            self.splash.append(RoundRect(i * 35 + 105, 240, 25, 25, 3, outline=0xFFFFFF))

            text_group = displayio.Group(scale=2, x=i * 35 + 111, y=252)
            text_group.append(label.Label(terminalio.FONT, text=self.layout[2][i], color=0xFFFFFF))
            self.splash.append(text_group)
            time.sleep(0.1)

        self.splash.append(Rect( 188, 80, 25, 3, fill=0xFFFFFF))
        self.splash.append(Rect( 228, 80, 25, 3, fill=0xFFFFFF))
        self.splash.append(Rect( 268, 80, 25, 3, fill=0xFFFFFF))

        self.highlight = [[],[],[]]
        for i in range(10):
            self.highlight[0].append(RoundRect(i * 35 + 70, 100, 25, 25, 3, outline=0xFFFF00))
        for i in range(9):
            self.highlight[1].append(RoundRect(i * 35 + 87, 170, 25, 25, 3, outline=0xFFFF00))
        for i in range(8):
            self.highlight[2].append(RoundRect(i * 35 + 105, 240, 25, 25, 3, outline=0xFFFF00))
        self.splash.append(self.highlight[0][0])
        self.xindex = 0
        self.yindex = 0
        self.count = 0
        self.character = []
    
    def useKeyboard(self, direction):
        self.splash.remove(self.highlight[self.yindex][self.xindex])
        if direction == 'D':
            if self.yindex != 2:
                if self.yindex == 0:
                    if self.xindex == 9:
                        self.xindex = 8
                if self.yindex == 1:
                    if self.xindex == 8:
                        self.xindex = 7
                self.yindex = self.yindex + 1
        if direction == 'L':
            if self.xindex != 0:
                self.xindex = self.xindex - 1
        if direction == 'R':
            if self.yindex == 0:
                if self.xindex != 9:
                    self.xindex = self.xindex + 1
            if self.yindex == 1:
                if self.xindex != 8:
                    self.xindex = self.xindex + 1
            if self.yindex == 2:
                if self.xindex != 7:
                    self.xindex = self.xindex + 1
        if direction == 'U':
            if self.yindex != 0:
                self.yindex = self.yindex - 1
        self.splash.append(self.highlight[self.yindex][self.xindex])
        if direction == 'A':
            self.character.append(self.layout[self.yindex][self.xindex])
            text_group = displayio.Group(scale=2, x=self.count*40 + 193, y= 70)
            text_group.append(label.Label(terminalio.FONT, text=self.character[self.count], color=0xFFFFFF))
            self.splash.append(text_group)
            self.count = self.count + 1

        if self.count == 3:
            time.sleep(1)
            return 3
        else:
            return 5
            
    
    def homeOutline(self, i):
        self.splash.remove(self.highlight)
        if(i == 0):
            self.highlight = RoundRect(10, 120, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)
        elif(i == 1):
            self.highlight = RoundRect(10, 190, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)
        else:
            self.highlight = RoundRect(10, 260, 300, 50, 5, outline = 0xFFFF00)
            self.splash.append(self.highlight)


    def useHome(self, direction):
        if direction == 'U':
            if(self.yindex > 0):
                self.yindex = self.yindex - 1
                self.homeOutline(self.yindex)
        if direction == 'D':
            if(self.yindex < 2):
                self.yindex = self.yindex + 1
                self.homeOutline(self.yindex)
        if direction == 'A':
            if(self.yindex == 0):
                return 2
            if(self.yindex == 1):
                return 4
            if(self.yindex == 2):
                return 3
            
        p = self.ts.touch_point
        if p:
            x, y, pressure = p
            if(x > 160  and x < 480 and y > 110 and y < 180):
                self.homeOutline(1)
                return 2
    
            if(x > 160  and x < 480 and y > 180 and y < 250):
                self.homeOutline(2)
                return 4
                
            if(x > 160  and x < 480 and y > 250 and y < 320):
                self.homeOutline(3)
                return 3
        return 1
    
    def useLeaderboard(self, direction):
        if direction == 'A' or direction == 'B':
            return 1
        p = self.ts.touch_point
        if p:
            x, y, pressure = p
            if(x > 20  and x < 120 and y > 240 and y < 310):
                return 1
        return 3
            
        

    def clearMem(self):
        self.splash = None
        gc.collect()
        self.splash = displayio.Group()
        self.display.root_group = self.splash



        