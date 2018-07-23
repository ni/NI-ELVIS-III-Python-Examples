"""
NI ELVIS III Pulse Width Modulation Example 
This example illustrates how to generate a Pulse Width Modulation (PWM) signal
to an external peripheral through the PWM channels. The program first defines
the configuration for the PWM channels, then generates the signal for 20
seconds.

The PWM configuration consists of two parameters: bank and channel. There are
two identical banks of PWM channels (A and B). The PWM shared the same channels
with DIO. Each bank contains 19 digital input and output channels.

This example uses:
    Bank B, Channel DIO0.

Hardware setup:
    No hardware is needed.

Result:
    Generate a PWM signal from DIO0 on bank B.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Bank, DIOChannel

# specify the bank and channel for the PWM session
bank = Bank.B
channel = DIOChannel.DIO0

# open a PWM session
with academicIO.PWM(bank, channel) as PWM:
    # specify the frequency (integer value) settings for the PWM signal
    frequency = 1000
    # specify the percentage of time the PWM signal remains high over one PWM
    # cycle
    duty_cycle = 0.7

    # generate the PWM signal
    PWM.generate(frequency, duty_cycle)
    # begin to generate PWM signal for 20 seconds
    time.sleep(20)
    # stop generating PWM signal
