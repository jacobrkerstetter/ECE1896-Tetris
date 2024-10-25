"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
from display.display import *
from algorithm.game import *

state = 1

while True:
    # Intro Screen State
    if (state == 1):
        state = display.state1()

    # Gameplay State
    if (state == 2):
        # reset screen
        display.state2()

        # initialize game
        game = Game()
        while game.run:
            # clear memory when new piece drops in
            if game.changePiece:
                display.newPiece()

            display.displayBoard(game.board)
            nextPiece = game.nextPiece

            # update game
            game.updateFallingBlock()
            game.getNextBlock()

        # when game is over, go to leaderboard
        state = 3

    if (state == 3):
        state = display.state3()