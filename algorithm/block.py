from color import Color

# parent class for the game pieces

class Block:
    pieceCount = 1

    def __init__(self, color):
        # set id of piece to current count, increment count by 1
        self.id = Block.pieceCount
        Block.pieceCount += 1

        self.color = color
        self.cells = {}
        self.rotation = 0

    def move(self, board, rowOffset, colOffset):
        # clear all spaces previously filled
        for i in range(len(self.cells[self.rotation])):
            board.draw(self.cells[self.rotation][i][0], self.cells[self.rotation][i][1], 0)

        # update all rotation states and fill new blocks if rotation state matches current state
        for rotation in self.cells:
            for i in range(len(self.cells[rotation])):
                self.cells[rotation][i] = (self.cells[rotation][i][0] + rowOffset, self.cells[rotation][i][1] + colOffset)

                if self.rotation == rotation:
                    board.draw(self.cells[self.rotation][i][0], self.cells[self.rotation][i][1], self.color) 
    
    def rotate(self, board):
        # clear all spaces previously filled
        for i in range(len(self.cells[self.rotation])):
            board.draw(self.cells[self.rotation][i][0], self.cells[self.rotation][i][1], 0)

        if self.rotation == 3:
            self.rotation = 0
        else:
            self.rotation += 1

        self.move(board, 0, 0)
    
# child classes for each piece
class JBlock(Block):
    def __init__(self, board):
        super().__init__(Color.colors['lightBlue'])
        self.cells = {
            0: [(0,0), (1,0), (1,1), (1,2)],
            1: [(0,2), (0,1), (1,1), (2,1)],
            2: [(1,0), (1,1), (1,2), (2,2)],
            3: [(0,1), (1,1), (2,0), (2,1)], 
        }

        self.move(board, 0, 0)

class LBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['orange'])

class IBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['darkBlue'])

class SBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['green'])

class TBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['purple'])

class ZBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['red'])

class OBlock(Block):
    def __init__(self, color):
        super.__init__(Color.colors['yellow'])