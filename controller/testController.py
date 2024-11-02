'''
ECE1896 Senior Design
Tetris Controller Program
Written by Cassandra Oliva Pace
'''

import board
import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer


# create object for each controller button and assign pin on Teensy
pin2 = DigitalInOut(board.D2)
pin3 = DigitalInOut(board.D3)
pin4 = DigitalInOut(board.D4)
pin5 = DigitalInOut(board.D5)

# define direction of pins
pin2.direction = Direction.INPUT
pin3.direction = Direction.INPUT
pin4.direction = Direction.INPUT
pin5.direction = Direction.INPUT

# set button input pins to be pulled low when line isn't being driven
pin2.pull = Pull.DOWN
pin3.pull = Pull.DOWN
pin4.pull = Pull.DOWN
pin5.pull = Pull.DOWN

# create objects for debouncing
upButton = Debouncer(pin2, interval=0.15)
rightButton = Debouncer(pin3, interval=0.15)
downButton = Debouncer(pin4, interval=0.15)
leftButton = Debouncer(pin5, interval=0.15)


while True:

    upButton.update()
    rightButton.update()
    downButton.update()
    leftButton.update()

    if upButton.value == True:
        print("Up")
    elif rightButton.value == True:
        print("Right")
    elif downButton.value == True:
        print("Down")
    elif leftButton.value == True:
        print("Left")



''' THINGS TO DO:
- what happens when user presses two or more buttons at once?
    - if you want both actions of both buttons done simulataneously, include individual IF statements
    without ELSE
    - if you want only one action done at a time, use the ELSE statement
    (however, notice that this will prioritize the buttons in the order of their IF statements
- how to disable buttons when in certain menus?
'''