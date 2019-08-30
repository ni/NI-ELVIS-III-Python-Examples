"""
Hardware setup:
  To see the result, connect connector A DIO13 (where the output signal is) to a logic analyzer.
"""
import time
from nielvis import PWM, Bank, DIOChannel

bank = Bank.A
channel = DIOChannel.DIO13
with PWM(bank, channel) as pwm:
    frequency = 1200
    duty_cycle = 0.1
    pwm.generate(frequency, duty_cycle)

    print("Outputting PWM signal..")
    print("You can use a logic analyzer to check the output signal.")
    print("Press Ctrl+Z to stop.")
    while(True):
        time.sleep(0.01)