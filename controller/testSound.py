# ----------------------------------------------------------------------------------------------------------------------------------------
# Sound/Speaker Program for TESTING - PLEASE DO NOT EDIT THIS DIRECTLY

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
import audiocore
import audiobusio
#import array

# Connect to the card and mount the filesystem.
spi = bitbangio.SPI(board.CLK, board.CMD, board.DAT0)
cs = digitalio.DigitalInOut(board.DAT3)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

#buffer = array.array('B', [0]*1024)

# open and read the .txt file containing the top scores
with open("/sd/StreetChicken.wav", "rb") as file:
    
    soundWav = audiocore.WaveFile(file)
    # I2SOut(Bitclk, LRclk, data)
    a = audiobusio.I2SOut(board.D4, board.D3, board.D2)

    print("playing")
    a.play(soundWav)
    while a.playing:
        pass
    print("stopped")