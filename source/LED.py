"""
NI ELVIS III LED Example
This example illustrates how to set the status of the LEDs on the NI ELVIS III.
The program first defines the configuration for the LED session, then writes
to the LED register in a loop. Each time the write is called a Boolean data is
written to the register. The time between reads is not precisely timed, and is
controlled by a software delay.

This example uses:
    LED0.

Hardware setup:
    No hardware is needed.

Result:
    The LED flashes.
"""
import time
import academicIO
from enums import Led

# open an LED session
with academicIO.LEDs() as LED:
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on = True
    led_off = False
    # writes values 20 times
    for x in range(0, 20):
        # turn LED0 on
        LED.write(led, led_on)
        # add a short delay before acquiring next data point
        time.sleep(1)
        # turn LED0 off
        LED.write(led, led_off)
        # add a short delay before acquiring next data point
        time.sleep(1)
