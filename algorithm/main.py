import curses
from time import sleep

from board import Board
from block import *

def main( stdscr ):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    board = Board()
    for row in range(board.numRows):
        for col in range(board.numCols):
            stdscr.addstr(row, col, str(board.grid[row][col]))

    testBlock = JBlock(board)
    while True:
        stdscr.clear()
        stdscr.move(0, 0)

        for row in range(board.numRows):
            for col in range(board.numCols):
                stdscr.addstr(row, col, str(board.grid[row][col]))
        
        while True:
            key = stdscr.getch()
            if key == curses.KEY_DOWN:
                testBlock.move(board, 1, 0)
            if key == curses.KEY_LEFT:
                testBlock.move(board, 0, -1)
            if key == curses.KEY_RIGHT:
                testBlock.move(board, 0, 1)

            for row in range(board.numRows):
                for col in range(board.numCols):
                    stdscr.addstr(row, col, str(board.grid[row][col]))

        stdscr.refresh()

curses.wrapper( main )