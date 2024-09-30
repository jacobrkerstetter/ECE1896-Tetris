import curses
import pygame
import random

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

    # list of game piece options
    pieces = [JBlock, SBlock, ZBlock, OBlock, LBlock, TBlock, IBlock]
    currPiece = JBlock(board)
    currPiece.draw()
    nextPiece = random.choice(pieces)(board)
    
    # control vars for game loop
    run = True
    changePiece = False

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
            currPiece.move(1, 0)

            # if piece touches bottom, change flag
            for cell in currPiece.cells[currPiece.rotation]:
                if cell[0] == 19:
                    changePiece = True

        # get user input to move piece
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            currPiece.move(1, 0)
        if key == curses.KEY_LEFT:
            currPiece.move(0, -1)
        if key == curses.KEY_RIGHT:
            currPiece.move(0, 1)
        if key == curses.KEY_UP:
            currPiece.rotate()

        # if piece hits bottom, start with new piece
        if changePiece:
            currPiece = nextPiece
            currPiece.draw()

            nextPiece = random.choice(pieces)(board)

            changePiece = False

curses.wrapper( main )