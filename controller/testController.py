'''
ECE1896 Senior Design
Tetris Controller Program
Written by Cassandra Oliva Pace
'''

# TO DO: how to disable buttons when in certain menus?

import board
import keypad
import supervisor


buttons = keypad.Keys((board.D2, board.D3, board.D4, board.D5, board.D6, board.D7), value_when_pressed = True, pull = True, interval = 0.05, max_events = 1)
currentEvent = keypad.Event()

upButton = keypad.Event(0, True)  # Button D2 pressed
rightButton = keypad.Event(1, True)  # Button D3 pressed
downButton = keypad.Event(2, True)  # Button D4 pressed
leftButton = keypad.Event(3, True)  # Button D5 pressed
rotateButton = keypad.Event(4, True)  # Button D6 pressed
dropButton = keypad.Event(5, True)  # Button D7 pressed


while True:
    
    if buttons.events.get_into(currentEvent): # if an event is available in the queue
        
        lastTime = currentEvent.timestamp

        if currentEvent == upButton: # up button is pressed
            print("Up")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected             
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Up")
                    lastTime = supervisor.ticks_ms()

        elif currentEvent == rightButton: # right button is pressed
            print("Right")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected              
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Right")
                    lastTime = supervisor.ticks_ms()

        elif currentEvent == downButton: # down button is pressed
            print("Down")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected               
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Down")
                    lastTime = supervisor.ticks_ms()

        elif currentEvent == leftButton: # left button is pressed
            print("Left")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected             
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Left")
                    lastTime = supervisor.ticks_ms()

        elif currentEvent == rotateButton: # rotate button is pressed
            print("Rotate")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected       
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Rotate")
                    lastTime = supervisor.ticks_ms()

        elif currentEvent == dropButton: # hard drop button is pressed
            print("Hard Drop")
            while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected  
                if supervisor.ticks_ms() - lastTime >= 250:
                    print("Hard Drop")
                    lastTime = supervisor.ticks_ms()