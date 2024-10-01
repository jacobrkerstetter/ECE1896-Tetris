# class to describe the gameboard layout

class Board:
    def __init__(self):
        self.numRows = 20
        self.numCols = 10
        self.grid = [[0 for j in range(self.numCols)] for i in range(self.numRows)]

    def printBoard(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                print(self.grid[row][col], end=' ')
            print('\r')

    def isCellEmpty(self, row, col):
        return self.grid[row][col] == 0
    
    def clear(self):
        self.grid = [[[0] * self.numCols] for i in range(self.numRows)]
    
    def isRowFull(self, row):
        for col in range(self.numCols):
            if self.isCellEmpty(row, col):
                return False
            
        return True
    
    def clearRows(self):
        for i, row in enumerate(self.grid):
            if 0 not in row:
                self.grid = [[0 for j in range(self.numCols)]] + self.grid[:i] + self.grid[i + 1:]

    def draw(self, row, col, color):
        self.grid[row][col] = color