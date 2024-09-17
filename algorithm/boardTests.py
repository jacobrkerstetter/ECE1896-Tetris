import unittest
from board import Board

class TestBoardMethods(unittest.TestCase):
    def testCellEmptyOnStartup(self):
        board = Board()

        for row in range(20):
            for col in range(10):
                self.assertTrue(board.isCellEmpty(row, col))

if __name__ == '__main__':
    unittest.main()