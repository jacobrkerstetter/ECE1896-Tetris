from board import Board
from block import *

board = Board()
testBlock = JBlock()

rotationState = 0
for cell in testBlock.cells[rotationState]:
    board.draw(cell[0], cell[1], testBlock.color)

board.printBoard()
board.clear()

print('\n\n-----------\n\n')

rotationState = 1
for cell in testBlock.cells[rotationState]:
    board.draw(cell[0], cell[1], testBlock.color)

board.printBoard()

board.clear()

print('\n\n-----------\n\n')

rotationState = 2
for cell in testBlock.cells[rotationState]:
    board.draw(cell[0], cell[1], testBlock.color)

board.printBoard()

board.clear()

print('\n\n-----------\n\n')

rotationState = 3
for cell in testBlock.cells[rotationState]:
    board.draw(cell[0], cell[1], testBlock.color)

board.printBoard()