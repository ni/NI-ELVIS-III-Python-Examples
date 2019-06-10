"""
NI ELVIS III Pulse Width Modulation Example 
This example illustrates how to generate a Pulse Width Modulation (PWM) signal
to an external peripheral through the PWM channels. The program first defines
the configuration for the PWM channels, and then generates the signal for 20
seconds.

The PWM configuration consists of two parameters: bank and channel. There are
two identical banks of PWM channels (A and B). The PWM shares the same channels
with DIO. Each bank contains 20 digital input and output channels.

This example uses:
    Bank B, Channel DIO0.

Hardware setup:
    No hardware is needed.

Result:
    Generate a PWM signal from DIO0 on bank B.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'source/nielvisiii'))

import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank and channel for the PWM session
bank = Bank.B
channel = DIOChannel.DIO0

# configure a PWM session
with academicIO.PWM(bank, channel) as PWM:
    # specify the frequency (floating-point number) for the PWM signal. The
    # FPGA automatically coerces it to the nearest possible frequency.
    frequency = 1000
    # specify the percentage of time the PWM signal remains high over one PWM
    # cycle
    duty_cycle = 0.7

    # generate the PWM signal
    PWM.generate(frequency, duty_cycle)
    # begin to generate the PWM signal for 20 seconds
    time.sleep(20)
# stop generating the PWM signal when the 'with' statement ends
