'''
ECE1896 Senior Design
Tetris Controller Program
Written by Cassandra Oliva Pace
'''

import board
import digitalio
import keypad
import time

# create object for each controller button and assign pin on Teensy
upButton = digitalio.DigitalInOut(board.D2)
rightButton = digitalio.DigitalInOut(board.D3)
downButton = digitalio.DigitalInOut(board.D4)
leftButton = digitalio.DigitalInOut(board.D5)

# define direction of pins
upButton.direction = digitalio.Direction.INPUT
rightButton.direction = digitalio.Direction.INPUT
downButton.direction = digitalio.Direction.INPUT
leftButton.direction = digitalio.Direction.INPUT

# set button input pins to be pulled low when line isn't being driven
upButton.pull = digitalio.Pull.DOWN
rightButton.pull = digitalio.Pull.DOWN
downButton.pull = digitalio.Pull.DOWN
leftButton.pull = digitalio.Pull.DOWN


while True:

    if upButton.value == True:
        print("Up")
        time.sleep(0.2) # this is used as debouncing for pushbuttons
    elif rightButton.value == True:
        print("Right")
        time.sleep(0.2)
    elif downButton.value == True:
        print("Down")
        time.sleep(0.2)
    elif leftButton.value == True:
        print("Left")
        time.sleep(0.2)



''' THINGS TO DO:
- what happens when user presses two or more buttons at once?
    - if you want both actions of both buttons done simulataneously, include individual IF statements
    without ELSE
    - if you want only one action done at a time, use the ELSE statement
    (however, notice that this will prioritize the buttons in the order of their IF statements
- how to disable buttons when in certain menus?
'''