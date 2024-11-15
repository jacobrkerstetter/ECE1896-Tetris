# ----------------------------------------------------------------------------------------------------------------------------------------
# Memory Program for INTEGRATION - Feel free to edit as needed

# ECE 1896 Senior Design
# Written by Cassandra Oliva Pace
# ----------------------------------------------------------------------------------------------------------------------------------------

import os
import board
import storage
import busio
import digitalio
import adafruit_sdcard
import bitbangio

class Memory:
    def __init__(self):

        # Connect to the card and mount the filesystem.
        spi = bitbangio.SPI(board.CLK, board.CMD, board.DAT0)
        cs = digitalio.DigitalInOut(board.DAT3)
        sdcard = adafruit_sdcard.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
  
        # open and read the .txt file containing the top scores
        with open("/sd/TetrisScores.txt", "r+") as self.file:

            self.scoreList = self.file.readlines() # scoreList is a python list() object # lines is a python list() object

            self.scoreUseList = [0,0,0,0,0,0,0,0,0,0]
            for i in range(10):
                self.scoreUseList[i] = self.scoreList[i].strip()



    # ********************* FOR LEADERBOARD DISPLAY *********************
    def returnScores(self):
        return self.scoreUseList
    

    def updateScores(self, newScore, tag):

        nums = []

        for i in range(10):
            nums.append(int(self.scoreUseList[i][0:8]))

        place = 10
        for i in range(9, -1, -1):
            if newScore > nums[i]:
                place = i

        newScoreSTR = f"{newScore:08}" # converts the score to a string and pads it with zeros until it is 8 chars long

        print(self.scoreList)
        self.scoreList.insert(place, newScoreSTR + " " + tag + "\n")
        self.scoreUseList.insert(place, newScoreSTR + " " + tag)
        print(self.scoreList)

        with open("/sd/TetrisScores.txt", "r+") as self.file:
            self.file.seek(0)
            print(self.scoreList)
            for i in range(10):
                print(self.scoreList[i])
                self.file.write(self.scoreList[i])

    def newTopTen(self, score):
        return score > int(self.scoreUseList[9][0:8])