"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
from display.display import *
from algorithm.game import *
from controller.userInput import *

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
        userControls = UserInput()
        while game.run:
            display.displayBoard(game.board.grid, game.nextPiece)

            # update game
            game.updateFallingBlock()

            # get user input
            input = userControls.pollInput()
            if input == 'D':
                game.currPiece.move(1, 0)
            if input == 'L':
                game.currPiece.move(0, -1)
            if input == 'R':
                game.currPiece.move(0, 1)
            if input == 'U':
                game.currPiece.rotate()

            game.getNextBlock()

        # when game is over, go to leaderboard
        state = 3

    if (state == 3):
        state = display.state3()

    if (state == 4):
        state = display.state4()

    if (state == 5):
        state = display.state5()