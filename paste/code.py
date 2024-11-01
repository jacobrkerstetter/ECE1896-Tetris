"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
from display.display import *
from algorithm.game import *
from controller.userInput import *

state = 1

while True:
    # Intro Screen State
    if (state == 1):
        state = state1()

    # Gameplay State
    if (state == 2):
        # reset screen
        state2()

        # initialize game and controls
        game = Game()
        userControls = UserInput()
        while game.run:
            displayBoard(game.board.grid)

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
        state = state3()