# ----------------------------------------------------------------------------------------------------------------------------------------
# Memory Program for TESTING - PLEASE DO NOT EDIT THIS DIRECTLY

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

# the following two modules are imported only for testing purposes
import sys
import time

# ----------------------------------------------------------------------------------------------------------------------------------------
# Notes on the organization of the scores file:
#   - only the top 10 scores are saved, therefore the text file contains only 10 lines of text, each representing a score
#   - each line contains the player's name/tag, followed by a SPACE character, then the score number, and finally a NEWLINE character

# TO DO:
# To correctly format .txt file and display nicely, should there be a SPACE char or a TAB char?
# ----------------------------------------------------------------------------------------------------------------------------------------


# Connect to the card and mount the filesystem.
spi = bitbangio.SPI(board.CLK, board.CMD, board.DAT0)
cs = digitalio.DigitalInOut(board.DAT3)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


# open and read the .txt file containing the top scores
with open("/sd/TetrisScores.txt", "r+") as file:
    
    # ********************* FOR LEADERBOARD DISPLAY *********************
    contents = file.read() # lines is a python list() object
    print(contents)
        
    # alternative method for displaying:
    #for line in file: # display all scores
    #    print(line.strip()) # strip() removes trailing newlines
    

    # ********************* UPDATE SCORES *********************
    
    file.seek(0) # Go back to the beginning of the file
    scoreList = file.readlines() # scoreList is a python list() object
    
    newScore = 75
    newName = "new"

    nums = []

    for i in range(10):
        nums.append(int(scoreList[i][0:8]))

    place = 10
    for i in range(9, -1, -1):
        if newScore > nums[i]:
            place = i

    newScoreSTR = f"{newScore:08}" # converts the score to a string and pads it with zeros until it is 8 chars long

    scoreList.insert(place, newScoreSTR + " " + newName + "\n")

    file.seek(0)
    
    for i in range(10):
        file.write(scoreList[i])


    '''
    file.seek(0)
    for item in scoreList:
        file.write(item)
    
    file.seek(0)
    contents = file.read() # lines is a python list() object
    print(contents)
    '''



'''
--------------------------------------------------------------------------------------------------------------------------
SDCARDIO IMPLEMENTATION
(this should be the correct way to access the SD card but CircuitPython has the wrong SD card interface built in!!!)
--------------------------------------------------------------------------------------------------------------------------

import sdcardio

# initialize an object for the SD card and mount it
sdcard = sdcardio.SDCard(board.SPI(), board.D44) # pin D44 on the teensy is CS2
vfs = storage.VfsFat(sdcard) # create a new filesystem around the SD card device
storage.mount(vfs, '/sd', False) # mounts the filesystem at the given path; False makes it read AND write
'''
