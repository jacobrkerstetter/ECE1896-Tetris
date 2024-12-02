"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import digitalio
import keypad
import time
import supervisor

from algorithm.game import RiggedGame
from display.display import *
from algorithm.game import *
from algorithm.game import *
from controller.memory import *
#from controller.userInput import *

# instatiate inputs
# create a keys object for all controller button pins
buttons = keypad.Keys((board.D16, board.D19, board.D18, board.D17, board.D21, board.D20), value_when_pressed = True, pull = True, interval = 0.05, max_events = 1)
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
memory = Memory()

while True:
    # Intro Screen State
    if (state == 1):
        timePressed = time.monotonic()
        display.state1()
        timeDone = time.monotonic()
        print('Home Latency: {}'.format(timeDone-timePressed))
        while(state == 1):
            timePressed = time.monotonic()
            if buttons.events.get_into(currentEvent): # if an event is available in the queue
                lastTime = currentEvent.timestamp
                input = ' '
                if currentEvent == upButton: # up button is pressed
                    input = 'U'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == downButton: # up button is pressed
                    input = 'D'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == dropButton: # up button is pressed
                    input = 'A'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                state = display.useHome(input)
            else:
                state = display.useHome(' ')
        timeDone = time.monotonic()
        print('Touch Latency: {}'.format(timeDone-timePressed))

    # Gameplay State
    if (state == 2):
        # reset screen
        timePressed = time.monotonic()
        display.state2()
        timeDone = time.monotonic()
        print('GameStart Latency: {}'.format(timeDone-timePressed))

        # initialize game and controls
        game = Game(display)
        # userControls = UserInput()
        while game.run:
            display.displayBoard(game.board.grid, game.nextPiece)

            # update game
            game.updateFallingBlock()

            # get user input
            if buttons.events.get_into(currentEvent): # if an event is available in the queue
                lastTime = currentEvent.timestamp

                if currentEvent == upButton: # up button is pressed
                    game.currPiece.rotate()
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.rotate()
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

                elif currentEvent == rightButton: # right button is pressed
                    game.currPiece.move(0, 1)
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.move(0, 1)
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

                elif currentEvent == downButton: # down button is pressed
                    game.currPiece.move(1, 0)
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.move(1, 0)
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

                elif currentEvent == leftButton: # left button is pressed
                    game.currPiece.move(0, -1)
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.move(0, -1)
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

                elif currentEvent == rotateButton: # rotate button is pressed
                    game.currPiece.rotate()
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.rotate()
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

                elif currentEvent == dropButton: # hard drop button is pressed
                    game.currPiece.hardDrop()
                    display.displayBoard(game.board.grid, game.nextPiece)
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            game.currPiece.hardDrop()
                            game.updateFallingBlock()
                            display.displayBoard(game.board.grid, game.nextPiece)
                            lastTime = supervisor.ticks_ms()
                            game.getNextBlock()

            game.getNextBlock()

        # when game is over, go to leaderboard
        score = display.gameOver()
        if memory.newTopTen(score):
            state = 5
        else:
            state = 3

    if (state == 3):
        timePressed = time.monotonic()
        display.state3(memory.returnScores())
        timeDone = time.monotonic()
        print('Leader Latency: {}'.format(timeDone-timePressed))
        while(state == 3):
            if buttons.events.get_into(currentEvent): # if an event is available in the queue
                lastTime = currentEvent.timestamp
                input = ' '
                if currentEvent == rotateButton: # up button is pressed
                    input = 'B'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == dropButton: # up button is pressed
                    input = 'A'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                state = display.useLeaderboard(input)
            else:
                state = display.useLeaderboard(' ')

    if (state == 4):
        timePressed = time.monotonic()
        display.state4()
        timeDone = time.monotonic()
        print('Help Latency: {}'.format(timeDone-timePressed))
        while(state == 4):
            if buttons.events.get_into(currentEvent): # if an event is available in the queue
                lastTime = currentEvent.timestamp
                input = ' '
                if currentEvent == rotateButton: # up button is pressed
                    input = 'B'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == dropButton: # up button is pressed
                    input = 'A'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                state = display.useHelp(input)
            else:
                state = display.useHelp(' ')

    if (state == 5):
        timePressed = time.monotonic()
        display.state5()
        timeDone = time.monotonic()
        print('Keyboard Latency: {}'.format(timeDone-timePressed))
        while(state == 5):
            if buttons.events.get_into(currentEvent): # if an event is available in the queue
                lastTime = currentEvent.timestamp
                input = ' '
                if currentEvent == upButton: # up button is pressed
                    input = 'U'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == downButton: # down button is pressed
                    input = 'D'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == leftButton: # left button is pressed
                    input = 'L'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == rightButton: # right button is pressed
                    input = 'R'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == rotateButton: # rotate button is pressed
                    input = 'B'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                if currentEvent == dropButton: # drop button is pressed
                    input = 'A'
                    while buttons.events.get_into(currentEvent) == False: # loops until a button release is detected
                        if supervisor.ticks_ms() - lastTime >= 250:
                            lastTime = supervisor.ticks_ms()
                state = display.useKeyboard(input)
        [hold1, hold2] = display.getPlayer()
        memory.updateScores(hold1,hold2)
