import curses
from game import Game

def main():
    screen = curses.initscr()
    wScore = curses.newwin(5, 17, 6, 5)
    wBoard = curses.newwin(24, 22, 0, 27)
    wBoard.nodelay(True)
    wBoard.keypad(True)

    wScore.border()
    wBoard.border()

    wScore.addstr(1, 1, "SCORE:")
    wScore.addstr(2, 1, "LINES:")
    wScore.addstr(3, 1, "LEVEL:")
    wScore.refresh()
    
    wBoard.refresh()

    # # create test board for single line clears
    # for i in range(9):
    #     board.draw(19, i, 'l')

    # # create test board for double line clears
    # for i in range(9):
    #     board.draw(18, i, 'l')
    #     board.draw(19, i, 'l')

    # # create test board for losing game
    # for i in range(3, 20):
    #     for j in range(9):
    #         board.draw(i, j, 'l')

    game = Game()

    while game.run:
        # reset game board each loop
        wBoard.clear()
        wScore.addstr(1, 16 - len(str(game.score)), str(game.score))
        wScore.addstr(2, 16 - len(str(game.linesCleared)), str(game.linesCleared))
        wScore.addstr(3, 16 - len(str(game.level)), str(game.level))
        wScore.refresh()

        # draw game board
        for row in range(game.board.numRows):
            for col in range(game.board.numCols):
                wBoard.addstr(row, col, str(game.board.grid[row][col]))
        wBoard.refresh()
        
        game.updateFallingBlock()

        # get user input to move piece
        key = wBoard.getch()
        if key == ord('p'):
            game.pause = True
            while game.pause:
                newKey = wBoard.getch()
                if newKey == ord('p'):
                    game.pause = False
        if key == curses.KEY_DOWN:
            game.currPiece.move(1, 0)
        if key == curses.KEY_LEFT:
            game.currPiece.move(0, -1)
        if key == curses.KEY_RIGHT:
            game.currPiece.move(0, 1)
        if key == curses.KEY_UP:
            game.currPiece.rotate()

        game.getNextBlock()

        # pause screen for losing
        if not game.run:
            while True:
                pass
        
main()