# library imports
import pygame
import time
import random

# class imports
from board import Board
from block import *

class Game:
    def __init__(self):
        # initialize score to 0 and level to 1
        self.score = 0
        self.linesCleared = 0
        self.level = 1

        # set up pygame clock
        self.clock = pygame.time.Clock()
        self.fallTime = 0
        self.fallSpeed = 0.8

        # instatiate game board
        self.board = Board()

        # seed random generator
        random.seed(int(time.time()))

        # list of game piece options
        self.pieces = [JBlock, SBlock, ZBlock, OBlock, LBlock, TBlock, IBlock]

        # set up initial pieces
        self.currPiece = self.getRandomPiece()
        self.currPiece.draw()
        self.nextPiece = self.getRandomPiece()

        # control vars for game loop
        self.run = True
        self.changePiece = False
        self.pause = False

    # function to get new random piece
    def getRandomPiece(self):
        return random.choice(self.pieces)(self.board)

    # function to make block fall automatically
    def updateFallingBlock(self):
        self.fallTime += self.clock.get_rawtime()
        self.clock.tick()

        if self.fallTime / 1000 >= self.fallSpeed:
            self.fallTime = 0

            if not self.currPiece.move(1, 0):
                self.changePiece = True

    # function to decide whether to change piece
    def getNextBlock(self):
        # if piece cannot move down any further, start with new piece
        if self.changePiece:
            # clear rows that are full, track level and score
            numCleared = self.board.clearRows()
            self.linesCleared += numCleared
            if self.linesCleared % 10 == 0 and self.linesCleared != 0:
                self.level += 1
                # TODO: UPDATE SPEED
            self.score += self.updateScore(numCleared)

            # if nextPiece is overlapping a current piece, game over
            if not self.nextPiece.isValidSpace():
                self.run = False

            # make current piece the next piece in line and draw it
            self.currPiece = self.nextPiece
            self.currPiece.draw()

            # randomly choice a next piece
            self.nextPiece = self.getRandomPiece()
            self.changePiece = False

    # function to update score
    def updateScore(self, n):
        if n == 1:
            return 40 * (self.level + 1)
        elif n == 2:
            return 100 * (self.level + 1)
        elif n == 3:
            return 300 * (self.level + 1)
        elif n == 4:
            return 1200 * (self.level + 1)
        else:
            return 0