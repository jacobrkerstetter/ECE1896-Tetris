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
        # create a keys object for all controller button pins
        self.buttons = keypad.Keys((board.D2, board.D3, board.D4, board.D5, board.D6, board.D7), value_when_pressed = True, pull = True, interval = 0.05, max_events = 1)
        self.currentEvent = keypad.Event()

        # create events for each button to compare with
        self.upButton = keypad.Event(0, True)  # Button D2 pressed
        self.rightButton = keypad.Event(1, True)  # Button D3 pressed
        self.downButton = keypad.Event(2, True)  # Button D4 pressed
        self.leftButton = keypad.Event(3, True)  # Button D5 pressed
        self.rotateButton = keypad.Event(4, True)  # Button D6 pressed
        self.dropButton = keypad.Event(5, True)  # Button D7 pressed

    def pollInput(self):
        if self.buttons.events.get_into(self.currentEvent): # if an event is available in the queue
            self.lastTime = self.currentEvent.timestamp

            if self.currentEvent == self.upButton: # up button is pressed
                print("Up")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected             
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Up")
                        lastTime = supervisor.ticks_ms()

            elif self.currentEvent == self.rightButton: # right button is pressed
                print("Right")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected              
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Right")
                        lastTime = supervisor.ticks_ms()

            elif self.currentEvent == self.downButton: # down button is pressed
                print("Down")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected               
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Down")
                        lastTime = supervisor.ticks_ms()

            elif self.currentEvent == self.leftButton: # left button is pressed
                print("Left")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected             
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Left")
                        lastTime = supervisor.ticks_ms()

            elif self.currentEvent == self.rotateButton: # rotate button is pressed
                print("Rotate")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected       
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Rotate")
                        lastTime = supervisor.ticks_ms()

            elif self.currentEvent == self.dropButton: # hard drop button is pressed
                print("Hard Drop")
                while self.buttons.events.get_into(self.currentEvent) == False: # loops until a button release is detected  
                    if supervisor.ticks_ms() - lastTime >= 250:
                        print("Hard Drop")
                        lastTime = supervisor.ticks_ms()

        if self.upButton.value == True:
            time.sleep(0.2)
            return 'U'
        elif self.rightButton.value == True:
            time.sleep(0.2)
            return 'R'
        elif self.downButton.value == True:
            time.sleep(0.2)
            return 'D'
        elif self.leftButton.value == True:
            time.sleep(0.2)
            return 'L'

''' THINGS TO DO:
- what happens when user presses two or more buttons at once?
    - if you want both actions of both buttons done simulataneously, include individual IF statements
    without ELSE
    - if you want only one action done at a time, use the ELSE statement
    (however, notice that this will prioritize the buttons in the order of their IF statements
- how to disable buttons when in certain menus?
'''