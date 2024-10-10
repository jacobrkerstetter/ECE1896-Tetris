import unittest
from game import Game

class TestGameMethods(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.game = Game()

    def testInitialize(self):
        self.assertIsNotNone(self.game)

    def testLevelUpdateSingleClear(self):
        self.game.changePiece = True
        self.game.linesCleared = 9
        self.game.getNextBlock()

        # simulate 1 line cleared
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.level, 2)
        self.assertAlmostEqual(self.game.fallSpeed, 0.7)

    def testLevelUpdateMultiClear(self):
        self.game.changePiece = True
        self.game.linesCleared = 9
        self.game.getNextBlock()

        # simulate 2 lines cleared
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.level, 2)
        self.assertAlmostEqual(self.game.fallSpeed, 0.7)

    def test1LineClearScoreLevel1(self):
        # simulate 1 line cleared on level 1
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 80)

        # simulate 1 line cleared on level 2
        self.game.level = 2
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 200)

    def test2LineClearScore(self):
        # simulate 2 line cleared on level 1
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 200)

        # simulate 2 line cleared on level 2
        self.game.level = 2
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 500)

    def test3LineClearScore(self):
        # simulate 3 line cleared on level 1
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(17, i, 'l')
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 600)

        # simulate 3 line cleared on level 2
        self.game.level = 2
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(17, i, 'l')
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 1500)

    def test4LineClearScore(self):
        # simulate 4 line cleared on level 1
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(16, i, 'l')
            self.game.board.draw(17, i, 'l')
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 2400)

        # simulate 4 line cleared on level 2
        self.game.level = 2
        self.game.changePiece = True
        for i in range(10):
            self.game.board.draw(16, i, 'l')
            self.game.board.draw(17, i, 'l')
            self.game.board.draw(18, i, 'l')
            self.game.board.draw(19, i, 'l')
        self.game.getNextBlock()

        self.assertEqual(self.game.score, 6000)

if __name__ == '__main__':
    unittest.main()