'''
ECE1896 Senior Design
Tetris Controller Program
Written by Cassandra Oliva Pace
'''


import board
import digitalio
import keypad
import time

class UserInput:
    def __init__(self):
        # create object for each controller button and assign pin on Teensy
        self.upButton = digitalio.DigitalInOut(board.D2)
        self.rightButton = digitalio.DigitalInOut(board.D3)
        self.downButton = digitalio.DigitalInOut(board.D4)
        self.leftButton = digitalio.DigitalInOut(board.D5)

        # define direction of pins
        self.upButton.direction = digitalio.Direction.INPUT
        self.rightButton.direction = digitalio.Direction.INPUT
        self.downButton.direction = digitalio.Direction.INPUT
        self.leftButton.direction = digitalio.Direction.INPUT

        # set button input pins to be pulled low when line isn't being driven
        self.upButton.pull = digitalio.Pull.DOWN
        self.rightButton.pull = digitalio.Pull.DOWN
        self.downButton.pull = digitalio.Pull.DOWN
        self.leftButton.pull = digitalio.Pull.DOWN

    def pollInput(self):
        if self.upButton.value == True:
            print("Up")
            time.sleep(0.2) # this is used as debouncing for pushbuttons
        elif self.rightButton.value == True:
            print("Right")
            time.sleep(0.2)
        elif self.downButton.value == True:
            print("Down")
            time.sleep(0.2)
        elif self.leftButton.value == True:
            print("Left")
            time.sleep(0.2)