"""
NI ELVIS III Pulse Width Modulation (PWM) Example 
This example illustrates how to generate a PWM signal to an external 
peripheral through the PWM channels. To create a PWM session, you need to
define two required parameters, bank and channel. To configure a PWM signal,
you need to define another two required parameters, frequency and duty_cycle.

Hardware setup:
    No hardware is needed.

Result:
    Generate a PWM signal from DIO0 on bank B.
"""
import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank and channel for the PWM session
bank = Bank.B
channel = DIOChannel.DIO0

# open a PWM session, and set initial values for the parameters
with academicIO.PWM(bank, channel) as PWM:
    # specify the frequency settings for the PWM signal
    frequency = 160
    # specify the percentage of time the PWM signal remains high over one PWM
    # cycle
    duty_cycle = 0.7

    # generate the PWM signal
    PWM.configure(frequency, duty_cycle)
    # The program generates the PWM signal 20 times
    for i in range(0, 20):
            time.sleep(0.01)
            print "generating PWM signal.."