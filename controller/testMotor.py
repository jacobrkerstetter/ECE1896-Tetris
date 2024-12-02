# ----------------------------------------------------------------------------------------------------------------------------------------
# Vibration Motor Program for TESTING - PLEASE DO NOT EDIT THIS DIRECTLY

# ECE 1896 Senior Design
# Written by Cassandra Oliva Pace
# ----------------------------------------------------------------------------------------------------------------------------------------


import board
import digitalio
import pwmio
import time

EN = digitalio.DigitalInOut(board.D33)
EN.direction = digitalio.Direction.OUTPUT

pwm1 = pwmio.PWMOut(board.D36, frequency=100, duty_cycle = 2 ** 14) # Cycles the pin with 25% duty cycle (100% duty cycle is 2^16 or 2**16)
pwm2 = pwmio.PWMOut(board.D37, frequency=100, duty_cycle = 2 ** 14)

startMotor = time.monotonic()
while time.monotonic() - startMotor < 1:
    EN.value = True

EN.value = False

