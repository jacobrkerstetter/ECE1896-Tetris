import curses
import pygame

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
    currBlock = JBlock(board)
    nextPiece = JBlock(board)
    
    # control vars for game loop
    run = True

    while run:
        # reset game board each loop
        stdscr.clear()
        stdscr.move(0, 0)

        # draw game board
        for row in range(board.numRows):
            for col in range(board.numCols):
                stdscr.addstr(row, col, str(board.grid[row][col]))
        
        # code to govern dropping block automatically
        # fallTime += clock.get_rawtime()
        # clock.tick()

        # if fallTime / 1000 >= fallSpeed:
        #     fallTime = 0
        #     currBlock.move(1, 0)

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            currBlock.move(1, 0)
        if key == curses.KEY_LEFT:
            currBlock.move(0, -1)
        if key == curses.KEY_RIGHT:
            currBlock.move(0, 1)
        if key == curses.KEY_UP:
            currBlock.rotate()

curses.wrapper( main )