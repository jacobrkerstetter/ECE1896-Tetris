# ----------------------------------------------------------------------------------------------------------------------------------------
# Vibration Motor Program for INTEGRATION - Feel free to edit as needed

# ECE 1896 Senior Design
# Written by Cassandra Oliva Pace
# ----------------------------------------------------------------------------------------------------------------------------------------


import board
import digitalio
import pwmio
import time

class Motor:
    def __init__(self):
        self.EN = digitalio.DigitalInOut(board.D33)
        self.EN.direction = digitalio.Direction.OUTPUT

        # Set duty cycle as 25% (100% duty cycle is 2^16 or 2**16)
        pwm1 = pwmio.PWMOut(board.D36, frequency=100, duty_cycle = 2 ** 14) # motor 1 pwm signal
        pwm2 = pwmio.PWMOut(board.D37, frequency=100, duty_cycle = 2 ** 14) # motor 2 pwm signal


    def vibrate(self):
        startMotor = time.monotonic()
        
        while time.monotonic() - startMotor < 1:
            self.EN.value = True

        self.EN.value = False
