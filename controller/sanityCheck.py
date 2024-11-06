# ---------------------------------------------------------------------------------------------------------
# This file includes the most basic code for the controller to ensure all input buttons function correctly.
# If this code cannot properly run, there is something wrong with the hardware connections or the Teensy
# ---------------------------------------------------------------------------------------------------------

import board
import time
from digitalio import DigitalInOut, Direction, Pull

# create object for each controller button and assign pin on Teensy
pin2 = DigitalInOut(board.D2)
pin3 = DigitalInOut(board.D3)
pin4 = DigitalInOut(board.D4)
pin5 = DigitalInOut(board.D5)

# define direction of pins
pin2.direction = Direction.INPUT
pin3.direction = Direction.INPUT
pin4.direction = Direction.INPUT
pin5.direction = Direction.INPUT

# set button input pins to be pulled low when line isn't being driven
pin2.pull = Pull.DOWN
pin3.pull = Pull.DOWN
pin4.pull = Pull.DOWN
pin5.pull = Pull.DOWN

while True:
    
    if pin2.value == True:
        print("Up")
        time.sleep(0.2) # this is used as debouncing for pushbuttons
    elif pin3.value == True:
        print("Right")
        time.sleep(0.2)
    elif pin4.value == True:
        print("Down")
        time.sleep(0.2)
    elif pin5.value == True:
        print("Left")
        time.sleep(0.2)

