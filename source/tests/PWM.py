"""
Hardware setup:
  To see the result, connect connector A DIO13 (where the output signal is) to a logic analyzer.
"""
import time
import pytest
import academicIO
from enums import *

bank = Bank.A
channel = DIOChannel.DIO13
with academicIO.PWM(bank, channel) as PWM:
    frequency = 1200
    duty_cycle = 0.1
    PWM.configure(frequency, duty_cycle)
    # actual_frequency = PWM.configure(frequency, duty_cycle)
    # print actual_frequency
    # assert actual_frequency == pytest.approx(1200, 1)

    print "Outputting PWM signal.."
    print "You can use a logic analyzer to check the output signal."
    print "Press Ctrl+Z to stop."
    while(True):
        time.sleep(0.01)