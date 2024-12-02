# class to describe the gameboard layout

from controller.motor import Motor

class Board:
    def __init__(self, motor):
        self.numRows = 20
        self.numCols = 10
        self.grid = [['0' for j in range(self.numCols)] for i in range(self.numRows)]
        self.motor = motor

    def printBoard(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                pass
                #print(self.grid[row][col], end=' ')
            #print('\r')

    def isCellEmpty(self, row, col):
        return self.grid[row][col] == '0'
    
    def clear(self):
        self.grid = [['0' for j in range(self.numCols)] for i in range(self.numRows)]
    
    def clearRows(self):
        numCleared = 0
        for i, row in enumerate(self.grid):
            if '0' not in row:
                numCleared += 1
                self.motor.vibrate() # EDIT FROM CASSANDRA: vibrate motor
                self.grid = [['0' for j in range(self.numCols)]] + self.grid[:i] + self.grid[i + 1:]

        return numCleared

    def draw(self, row, col, color):
        self.grid[row][col] = color