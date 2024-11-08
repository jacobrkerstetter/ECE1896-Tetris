"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import digitalio
import keypad
import time

from display.display import *
from algorithm.game import *
from controller.userInput import *

# instatiate inputs
# create a keys object for all controller button pins
buttons = keypad.Keys((board.D2, board.D3, board.D4, board.D5, board.D6, board.D7), value_when_pressed = True, pull = True, interval = 0.05, max_events = 1)
currentEvent = keypad.Event()

# create events for each button to compare with
upButton = keypad.Event(0, True)  # Button D2 pressed
rightButton = keypad.Event(1, True)  # Button D3 pressed
downButton = keypad.Event(2, True)  # Button D4 pressed
leftButton = keypad.Event(3, True)  # Button D5 pressed
rotateButton = keypad.Event(4, True)  # Button D6 pressed
dropButton = keypad.Event(5, True)  # Button D7 pressed

state = 1
display = Display()

while True:
    # Intro Screen State
    if (state == 1):
        state = display.state1()

    # Gameplay State
    if (state == 2):
        # reset screen
        display.state2()

        # initialize game and controls
        game = Game(display)
        # userControls = UserInput()
        while game.run:
            display.displayBoard(game.board.grid, game.nextPiece)

        #     # update game
            game.updateFallingBlock()

        #     # get user input
        #     if buttons.events.get_into(currentEvent): # if an event is available in the queue
        #         lastTime = currentEvent.timestamp

        #         if currentEvent == upButton: # up button is pressed
        #             print("Up")
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected             
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     print("Up")
        #                     lastTime = supervisor.ticks_ms()

        #         elif currentEvent == rightButton: # right button is pressed
        #             game.currPiece.move(0, 1)
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected              
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     game.currPiece.move(0, 1)
        #                     lastTime = supervisor.ticks_ms()

        #         elif currentEvent == downButton: # down button is pressed
        #             game.currPiece.move(1, 0)
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected               
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     game.currPiece.move(1, 0)
        #                     lastTime = supervisor.ticks_ms()

        #         elif currentEvent == leftButton: # left button is pressed
        #             game.currPiece.move(0, -1)
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected             
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     game.currPiece.move(0, -1)
        #                     lastTime = supervisor.ticks_ms()

        #         elif currentEvent == rotateButton: # rotate button is pressed
        #             game.currPiece.rotate()
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected       
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     game.currPiece.rotate()
        #                     lastTime = supervisor.ticks_ms()

        #         elif currentEvent == dropButton: # hard drop button is pressed
        #             game.currPiece.hardDrop()
        #             while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected  
        #                 if supervisor.ticks_ms() - lastTime >= 250:
        #                     game.currPiece.hardDrop()
        #                     lastTime = supervisor.ticks_ms()

            game.getNextBlock()

        # when game is over, go to leaderboard
        state = 5

    if (state == 3):
        state = display.state3()

    if (state == 4):
        state = display.state4()

    if (state == 5):
        state = display.state5()
        state = 3