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

    # add test JBlock
    board = Board()
    testBlock = JBlock(board)

    while True:
        fallSpeed = 0.8

        stdscr.clear()
        stdscr.move(0, 0)

        # print board with test piece added
        for row in range(board.numRows):
            for col in range(board.numCols):
                stdscr.addstr(row, col, str(board.grid[row][col]))
        
        while True:
            fallTime += clock.get_rawtime()
            clock.tick()

            if fallTime / 1000 >= fallSpeed:
                fallTime = 0
                #testBlock.move(1, 0)

            key = stdscr.getch()
            if key == curses.KEY_DOWN:
                testBlock.move(1, 0)
            if key == curses.KEY_LEFT:
                testBlock.move(0, -1)
            if key == curses.KEY_RIGHT:
                testBlock.move(0, 1)
            if key == curses.KEY_UP:
                testBlock.rotate()

            for row in range(board.numRows):
                for col in range(board.numCols):
                    stdscr.addstr(row, col, str(board.grid[row][col]))

curses.wrapper( main )