# class to describe the gameboard layout

class Board:
    def __init__(self):
        self.numRows = 20
        self.numCols = 10
        self.grid = [[0] * self.numCols for i in range(self.numRows)]

    def printBoard(self):
        for i in range(self.numRows):
            for j in range(self.numCols):
                print(self.grid[i][j], end=' ')
            print()