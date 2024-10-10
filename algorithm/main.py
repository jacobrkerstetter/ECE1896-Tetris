import curses
from game import Game

def main( stdscr ):
    stdscr.clear()
    stdscr.nodelay(1)
    
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
        stdscr.clear()
        stdscr.move(0, 0)

        # draw game board
        for row in range(game.board.numRows):
            for col in range(game.board.numCols):
                stdscr.addstr(row, col, str(game.board.grid[row][col]))
        
        game.updateFallingBlock()

        # get user input to move piece
        key = stdscr.getch()
        if key == ord('p'):
            game.pause = True
            while game.pause:
                newKey = stdscr.getch()
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

curses.wrapper( main )