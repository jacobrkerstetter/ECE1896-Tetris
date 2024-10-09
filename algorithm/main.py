import curses
import pygame
import random
import time

from board import Board
from block import *

def main( stdscr ):
    stdscr.clear()
    stdscr.nodelay(1)

    # set up pygame clock
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.8

    # add test JBlock
    board = Board()
    
    # # create test board for single line clears
    # for i in range(9):
    #     board.draw(19, i, 'l')

    # # create test board for double line clears
    # for i in range(9):
    #     board.draw(18, i, 'l')
    #     board.draw(19, i, 'l')

    # # create test board for losing game
    # for i in range(3, 20):
    #     for j in range(9):
    #         board.draw(i, j, 'l')

    # seed random generator
    random.seed(int(time.time()))

    # list of game piece options
    pieces = [JBlock, SBlock, ZBlock, OBlock, LBlock, TBlock, IBlock]
    currPiece = random.choice(pieces)(board)
    #currPiece = IBlock(board)
    currPiece.draw()
    nextPiece = random.choice(pieces)(board)
    
    # control vars for game loop
    run = True
    changePiece = False
    pause = False

    while run:
        # reset game board each loop
        stdscr.clear()
        stdscr.move(0, 0)

        # draw game board
        for row in range(board.numRows):
            for col in range(board.numCols):
                stdscr.addstr(row, col, str(board.grid[row][col]))
        
        # code to govern dropping block automatically
        fallTime += clock.get_rawtime()
        clock.tick()

        if fallTime / 1000 >= fallSpeed:
            fallTime = 0

            if not currPiece.move(1, 0):
                changePiece = True

        # get user input to move piece
        key = stdscr.getch()
        if key == ord('p'):
            pause = True
            while pause:
                newKey = stdscr.getch()
                if newKey == ord('p'):
                    pause = False
        if key == curses.KEY_DOWN:
            currPiece.move(1, 0)
        if key == curses.KEY_LEFT:
            currPiece.move(0, -1)
        if key == curses.KEY_RIGHT:
            currPiece.move(0, 1)
        if key == curses.KEY_UP:
            currPiece.rotate()

        # if piece cannot move down any further, start with new piece
        if changePiece:
            # clear rows that are full
            board.clearRows()

            # if nextPiece is overlapping a current piece, game over
            if not nextPiece.isValidSpace():
                run = False

            # make current piece the next piece in line and draw it
            currPiece = nextPiece
            currPiece.draw()

            # randomly choice a next piece
            nextPiece = random.choice(pieces)(board)
            changePiece = False

        # pause screen for losing
        if not run:
            while True:
                pass

curses.wrapper( main )