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
    The LED0 flashes for 5 seconds.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Led

# configure an LED session
with academicIO.LEDs() as LED:
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True
    # writes values 10 times which turns LED1 on/off 5 times
    for x in range(0, 10):
        # turn LED0 on/off
        # the first parameter of the write function specifies which LED to
        # write to, the second parameter specifies the status of the LED which
        # should be either True or False
        LED.write(led, led_on_off)
        # add a short delay
        time.sleep(0.5)
        # if the led is on, set the paramter to off
        # if the led is off, set the paramter to on
        led_on_off = not led_on_off