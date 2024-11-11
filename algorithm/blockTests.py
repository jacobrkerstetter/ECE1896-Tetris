import unittest
from board import Board
from color import Color
from block import *

class TestBoardMethods(unittest.TestCase):

    def testJBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = JBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][4], 'l')
        self.assertEqual(board.grid[1][4], 'l')
        self.assertEqual(board.grid[1][5], 'l')
        self.assertEqual(board.grid[1][6], 'l')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'l')
        self.assertEqual(board.grid[1][5], 'l')
        self.assertEqual(board.grid[2][5], 'l')
        self.assertEqual(board.grid[0][6], 'l')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'l')
        self.assertEqual(board.grid[1][5], 'l')
        self.assertEqual(board.grid[1][6], 'l')
        self.assertEqual(board.grid[2][6], 'l')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[2][4], 'l')
        self.assertEqual(board.grid[0][5], 'l')
        self.assertEqual(board.grid[1][5], 'l')
        self.assertEqual(board.grid[2][5], 'l')

    def testLBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = LBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[1][4], 'o')
        self.assertEqual(board.grid[1][5], 'o')
        self.assertEqual(board.grid[1][6], 'o')
        self.assertEqual(board.grid[0][6], 'o')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'o')
        self.assertEqual(board.grid[1][5], 'o')
        self.assertEqual(board.grid[2][5], 'o')
        self.assertEqual(board.grid[2][6], 'o')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'o')
        self.assertEqual(board.grid[1][5], 'o')
        self.assertEqual(board.grid[1][6], 'o')
        self.assertEqual(board.grid[2][4], 'o')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][4], 'o')
        self.assertEqual(board.grid[0][5], 'o')
        self.assertEqual(board.grid[1][5], 'o')
        self.assertEqual(board.grid[2][5], 'o')

    def testIBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = IBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][4], 'd')
        self.assertEqual(board.grid[0][5], 'd')
        self.assertEqual(board.grid[0][6], 'd')
        self.assertEqual(board.grid[0][7], 'd')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][6], 'd')
        self.assertEqual(board.grid[1][6], 'd')
        self.assertEqual(board.grid[2][6], 'd')
        self.assertEqual(board.grid[3][6], 'd')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'd')
        self.assertEqual(board.grid[1][5], 'd')
        self.assertEqual(board.grid[1][6], 'd')
        self.assertEqual(board.grid[1][7], 'd')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'd')
        self.assertEqual(board.grid[1][5], 'd')
        self.assertEqual(board.grid[2][5], 'd')
        self.assertEqual(board.grid[3][5], 'd')

    def testSBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = SBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][5], 'g')
        self.assertEqual(board.grid[0][6], 'g')
        self.assertEqual(board.grid[1][5], 'g')
        self.assertEqual(board.grid[1][4], 'g')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'g')
        self.assertEqual(board.grid[1][5], 'g')
        self.assertEqual(board.grid[1][6], 'g')
        self.assertEqual(board.grid[2][6], 'g')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][5], 'g')
        self.assertEqual(board.grid[1][6], 'g')
        self.assertEqual(board.grid[2][4], 'g')
        self.assertEqual(board.grid[2][5], 'g')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][4], 'g')
        self.assertEqual(board.grid[1][4], 'g')
        self.assertEqual(board.grid[1][5], 'g')
        self.assertEqual(board.grid[2][5], 'g')

    def testTBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = TBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][5], 'p')
        self.assertEqual(board.grid[1][4], 'p')
        self.assertEqual(board.grid[1][5], 'p')
        self.assertEqual(board.grid[1][6], 'p')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'p')
        self.assertEqual(board.grid[1][5], 'p')
        self.assertEqual(board.grid[1][6], 'p')
        self.assertEqual(board.grid[2][5], 'p')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'p')
        self.assertEqual(board.grid[1][5], 'p')
        self.assertEqual(board.grid[1][6], 'p')
        self.assertEqual(board.grid[2][5], 'p')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'p')
        self.assertEqual(board.grid[0][5], 'p')
        self.assertEqual(board.grid[1][5], 'p')
        self.assertEqual(board.grid[2][5], 'p')

    def testZBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = ZBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][4], 'r')
        self.assertEqual(board.grid[0][5], 'r')
        self.assertEqual(board.grid[1][5], 'r')
        self.assertEqual(board.grid[1][6], 'r')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][6], 'r')
        self.assertEqual(board.grid[1][5], 'r')
        self.assertEqual(board.grid[1][6], 'r')
        self.assertEqual(board.grid[2][5], 'r')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[1][4], 'r')
        self.assertEqual(board.grid[1][5], 'r')
        self.assertEqual(board.grid[2][5], 'r')
        self.assertEqual(board.grid[2][6], 'r')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'r')
        self.assertEqual(board.grid[1][4], 'r')
        self.assertEqual(board.grid[1][5], 'r')
        self.assertEqual(board.grid[2][4], 'r')

    def testOBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = OBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][5], 'y')
        self.assertEqual(board.grid[0][6], 'y')
        self.assertEqual(board.grid[1][5], 'y')
        self.assertEqual(board.grid[1][6], 'y')

        # test rotation state 1 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'y')
        self.assertEqual(board.grid[0][6], 'y')
        self.assertEqual(board.grid[1][5], 'y')
        self.assertEqual(board.grid[1][6], 'y')

        # test rotation state 2 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'y')
        self.assertEqual(board.grid[0][6], 'y')
        self.assertEqual(board.grid[1][5], 'y')
        self.assertEqual(board.grid[1][6], 'y')

        # test rotation state 3 cells
        testBlock.rotate()
        self.assertEqual(board.grid[0][5], 'y')
        self.assertEqual(board.grid[0][6], 'y')
        self.assertEqual(board.grid[1][5], 'y')
        self.assertEqual(board.grid[1][6], 'y')

    def testMoveJBlock(self):
        board = Board()

        # add JBlock to grid
        testBlock = JBlock(board)
        testBlock.draw()

        # test rotation state 0 cells
        self.assertEqual(board.grid[0][4], 'l')
        self.assertEqual(board.grid[1][4], 'l')
        self.assertEqual(board.grid[1][5], 'l')
        self.assertEqual(board.grid[1][6], 'l')

        # move block down 1
        testBlock.move(1, 0)

        # test new block locations
        self.assertEqual(board.grid[0][4], '0')
        self.assertEqual(board.grid[1][5], '0')
        self.assertEqual(board.grid[1][6], '0')

        self.assertEqual(board.grid[1][4], 'l')
        self.assertEqual(board.grid[2][4], 'l')
        self.assertEqual(board.grid[2][5], 'l')
        self.assertEqual(board.grid[2][6], 'l')

    def testMoveJOffLeftScreenState1(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)
        testBlock.rotate()
        testBlock.move(0, -5)
        testBlock.move(0, -1)

        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[2][0], 'l')
        self.assertEqual(board.grid[0][1], 'l')
        
    def testMoveJOffLeftScreenState0(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        testBlock.move(0, -4)
        testBlock.move(0, -1)

        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[1][1], 'l')
        self.assertEqual(board.grid[1][2], 'l')

    def testMoveJOffRightScreen(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        testBlock.move(0, 3)
        self.assertEqual(board.grid[0][7], 'l')
        self.assertEqual(board.grid[1][7], 'l')
        self.assertEqual(board.grid[1][8], 'l')
        self.assertEqual(board.grid[1][9], 'l')

        testBlock.move(0, 1)
        self.assertEqual(board.grid[0][7], 'l')
        self.assertEqual(board.grid[1][7], 'l')
        self.assertEqual(board.grid[1][8], 'l')
        self.assertEqual(board.grid[1][9], 'l')

    def testRotateJOffLeftScreen(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)

        # move left to edge and attempt to rotate
        testBlock.move(0, -4)
        testBlock.rotate()
        testBlock.move(0, -1)
        testBlock.rotate()

        self.assertEqual(board.grid[0][0], 'l')
        self.assertEqual(board.grid[0][1], 'l')
        self.assertEqual(board.grid[1][0], 'l')
        self.assertEqual(board.grid[2][0], 'l')

    def testHardDrop(self):
        # add J Block to board
        board = Board()
        testBlock = JBlock(board)
        testBlock.hardDrop()

        self.assertEqual(board.grid[18][4], 'l')
        self.assertEqual(board.grid[19][4], 'l')
        self.assertEqual(board.grid[19][5], 'l')
        self.assertEqual(board.grid[19][6], 'l')

        testBlock = JBlock(board)
        testBlock.hardDrop()

        # check first block again
        self.assertEqual(board.grid[18][4], 'l')
        self.assertEqual(board.grid[19][4], 'l')
        self.assertEqual(board.grid[19][5], 'l')
        self.assertEqual(board.grid[19][6], 'l')

        # check new block
        self.assertEqual(board.grid[16][4], 'l')
        self.assertEqual(board.grid[17][4], 'l')
        self.assertEqual(board.grid[17][5], 'l')
        self.assertEqual(board.grid[17][6], 'l')
    
    def testHardDropClear2(self):
        # add J Block to board
        board = Board()
        # # create test board for double line clears
        for i in range(9):
            board.draw(18, i, 'l')
            board.draw(19, i, 'l')

        testBlock = IBlock(board)
        testBlock.rotate()
        testBlock.move(0,3)
        testBlock.hardDrop()

        board.clearRows()

        for i in range(9):
            self.assertEqual(board.grid[18][i], '0')
            self.assertEqual(board.grid[19][i], '0')

if __name__ == '__main__':
    unittest.main()