import curses
from game import Game
from color import Color

def main():
    screen = curses.initscr()

    # define colors
    curses.start_color()
    curses.use_default_colors()

    curses.init_color(1, 1000, 0, 0) # red
    curses.init_color(2, 0, 1000, 0) # green
    curses.init_color(3, 1000, 1000, 0) # yellow
    curses.init_color(4, 0, 0, 1000) # dark blue
    curses.init_color(5, 1000, 500, 1000) # pink
    curses.init_color(6, 500, 500, 1000) # light blue
    curses.init_color(7, 1000, 750, 325) # orange

    curses.init_pair(1, 1, 1) 
    curses.init_pair(2, 2, 2)
    curses.init_pair(3, 3, 3)
    curses.init_pair(4, 4, 4)
    curses.init_pair(5, 5, 5)
    curses.init_pair(6, 6, 6)
    curses.init_pair(7, 7, 7)

    # initialize and style windows
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
                if game.board.grid[row][col] != '0':
                    wBoard.addstr(row, col, str(game.board.grid[row][col]), curses.color_pair(Color.pairMap[game.board.grid[row][col]]))
                else:
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
        if key == ord('b'):
            game.currPiece.hardDrop()

        game.getNextBlock()

        # pause screen for losing
        if not game.run:
            while not game.reset:
                resetKey = wBoard.getch()
                if resetKey == ord('r'):
                    game.reset = True
        
            game.reset = False
            game.run = True
            game.resetGame()
        
main()