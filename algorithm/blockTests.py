import unittest
from board import Board
from color import Color
from block import *

class TestBoardMethods(unittest.TestCase):

    def testJBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = JBlock(board)
        rotationState = 0
        for cell in testBlock.cells[rotationState]:
            board.draw(cell[0], cell[1], testBlock.color)

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[1][1], 'l')
        self.assertEqual(board.grid[1][2], 'l')

    def testMoveJBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = JBlock(board)

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[1][1], 'l')
        self.assertEqual(board.grid[1][2], 'l')

        # move block down 1
        testBlock.move(1, 0)

        # test new block locations
        self.assertEqual(board.grid[0][0], 0)
        self.assertEqual(board.grid[1][1], 0)
        self.assertEqual(board.grid[1][2], 0)

        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[2][0], 'l')
        self.assertEqual(board.grid[2][1], 'l')
        self.assertEqual(board.grid[2][2], 'l')

    def testRotateJBlock(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        # rotate block
        testBlock.rotate()

        # test new block locations
        self.assertEqual(board.grid[0][0], 0)
        self.assertEqual(board.grid[1][0], 0)
        self.assertEqual(board.grid[1][2], 0)

        self.assertEqual(board.grid[0][1], 'l')
        self.assertEqual(board.grid[0][2], 'l')
        self.assertEqual(board.grid[1][1], 'l')
        self.assertEqual(board.grid[2][1], 'l')

    def testMoveOffLeftScreenState1(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)
        testBlock.rotate()
        testBlock.move(0, -1)

        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[2][0], 'l')
        self.assertEqual(board.grid[0][1], 'l')
        
    def testMoveOffLeftScreen(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        testBlock.move(0, -1)

        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[1][1], 'l')
        self.assertEqual(board.grid[1][2], 'l')

    def testMoveOffRightScreen(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        testBlock.move(0, 7)
        self.assertEqual(board.grid[0][7], 'l')
        self.assertEqual(board.grid[1][7], 'l')
        self.assertEqual(board.grid[1][8], 'l')
        self.assertEqual(board.grid[1][8], 'l')

        testBlock.move(0, 1)
        self.assertEqual(board.grid[0][7], 'l')
        self.assertEqual(board.grid[1][7], 'l')
        self.assertEqual(board.grid[1][8], 'l')
        self.assertEqual(board.grid[1][8], 'l')

    def testRotateOffLeftScreen(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        testBlock.rotate()
        testBlock.move(0, -1)
        testBlock.rotate()
        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[0][1], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[2][0], 'l')

if __name__ == '__main__':
    unittest.main()