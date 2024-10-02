from color import Color

# parent class for the game pieces

class Block:
    pieceCount = 1

    def __init__(self, color, board):
        # set id of piece to current count, increment count by 1
        self.id = Block.pieceCount
        Block.pieceCount += 1

        self.color = color
        self.cells = {}
        self.rotation = 0
        self.board = board

    def draw(self):
        for i in range(len(self.cells[self.rotation])):
            self.board.draw(self.cells[self.rotation][i][0], self.cells[self.rotation][i][1], self.color) 

    def clearCurrentPos(self):
        # clear current position to allow for block to be drawn in new location
        for i in range(len(self.cells[self.rotation])):
            self.board.draw(self.cells[self.rotation][i][0], self.cells[self.rotation][i][1], 0)

    def isValidSpace(self):
        validPositions = [[(i, j) for j in range(10) if self.board.grid[i][j] == 0] for i in range(20)]
        validPositions = [j for sub in validPositions for j in sub]

        for position in self.cells[self.rotation]:
            if position not in validPositions:
                return False
            
        return True

    def move(self, rowOffset, colOffset):
        # clear all spaces previously filled
        self.clearCurrentPos()

        # update all rotation states and fill new blocks if rotation state matches current state
        for rotation in self.cells:
            for i in range(len(self.cells[rotation])):
                self.cells[rotation][i] = (self.cells[rotation][i][0] + rowOffset, self.cells[rotation][i][1] + colOffset) 
        
        # check if the block is now in a valid location, if not move it back
        if not self.isValidSpace():
            for rotation in self.cells:
                for i in range(len(self.cells[rotation])):
                    self.cells[rotation][i] = (self.cells[rotation][i][0] - rowOffset, self.cells[rotation][i][1] - colOffset)

            valid = False
        else:
            valid = True

        self.draw() 
        return valid     
    
    def rotate(self):
        self.clearCurrentPos()
        self.rotation = (self.rotation + 1) % 4

        # check for valid movement before moving
        if not self.isValidSpace():
            self.rotation = (self.rotation - 1) % 4

        # clear all spaces previously filled
        self.draw()
    
# child classes for each piece
class JBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['lightBlue'], board)
        self.cells = {
            0: [(0,4), (1,4), (1,5), (1,6)],
            1: [(0,5), (1,5), (2,5), (0,6)],
            2: [(1,4), (1,5), (1,6), (2,6)],
            3: [(2,4), (0,5), (1,5), (2,5)], 
        }

class LBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['orange'], board)

        self.cells = {
            0: [(1,4), (1,5), (1,6), (0,6)],
            1: [(0,5), (1,5), (2,5), (2,6)],
            2: [(1,4), (1,5), (1,6), (2,4)],
            3: [(0,4), (0,5), (1,5), (2,5)], 
        }

class IBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['darkBlue'], board)

        self.cells = {
            0: [(1,4), (1,5), (1,6), (1,7)],
            1: [(0,6), (1,6), (2,6), (3,6)],
            2: [(2,4), (2,5), (2,6), (2,7)],
            3: [(0,5), (1,5), (2,5), (3,5)], 
        }

class SBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['green'], board)

        self.cells = {
            0: [(0,5), (0,6), (1,5), (1,4)],
            1: [(0,5), (1,5), (1,6), (2,6)],
            2: [(1,5), (1,6), (2,4), (2,5)],
            3: [(0,4), (1,4), (1,5), (2,5)], 
        }

class TBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['purple'], board)

        self.cells = {
            0: [(0,5), (1,4), (1,5), (1,6)],
            1: [(0,5), (1,5), (1,6), (2,5)],
            2: [(1,4), (1,5), (1,6), (2,5)],
            3: [(1,4), (0,5), (1,5), (2,5)], 
        }

class ZBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['red'], board)

        self.cells = {
            0: [(0,4), (0,5), (1,5), (1,6)],
            1: [(0,6), (1,5), (1,6), (2,5)],
            2: [(1,4), (1,5), (2,5), (2,6)],
            3: [(0,5), (1,4), (1,5), (2,4)], 
        }

class OBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['yellow'], board)

        self.cells = {
            0: [(0,5), (0,6), (1,5), (1,6)],
            1: [(0,5), (0,6), (1,5), (1,6)],
            2: [(0,5), (0,6), (1,5), (1,6)],
            3: [(0,5), (0,6), (1,5), (1,6)], 
        }