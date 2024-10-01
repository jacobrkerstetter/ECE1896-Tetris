import unittest
from board import Board
from color import Color

class TestBoardMethods(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.board = Board()
    
    def testCellEmptyOnStartup(self):
        # check that every cell in a 20x10 gameboard is empty on startup
        for row in range(20):
            for col in range(10):
                self.assertTrue(self.board.isCellEmpty(row, col))

    def testRowIsFull(self):
        # fill all bottom row cells and verify that the row is full
        colors = Color.getColorList()
        for col in range(10):
            self.board.draw(19, col, colors['red'])

        self.assertTrue(self.board.isRowFull(19))

    def testRowIsNotFull(self):
        colors = Color.getColorList()
        for col in range(10):
            self.board.draw(19, col, colors['red'])

        # set cell in (19,1) to empty
        self.board.draw(19, 1, 0)

        self.assertFalse(self.board.isRowFull(19))

    def testFillR1C1(self):
        # fill cell (1,1) with red and verify that the board holds that color
        colors = Color.getColorList()
        print()
        print(self.board.grid)
        print()
        self.board.draw(1, 1, colors['red'])

        self.assertFalse(self.board.isCellEmpty(1, 1))
        self.assertEqual(self.board.grid[1][1], 'r')
    
    def testClear1Row(self):
        # fill entire bottom row
        for i in range(10):
            self.board.draw(19, i, 'c')

        # call clearRows
        self.board.clearRows()

        # make sure bottom row is all 0s now
        for i in range(10):
            self.assertEqual(self.board.grid[19][i], 0)
        

if __name__ == '__main__':
    unittest.main()