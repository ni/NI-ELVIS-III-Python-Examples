"""
NI ELVIS III LED Example
This example illustrates how to set the status of the LEDs on the NI ELVIS III.
To create an LED session, you need to define led, which is an optional
parameter. The default value of led is LED0.

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
    # The program writes values 20 times
    for x in range(0, 20):
        # turn LED0 on
        LED.write(led, led_on)
        # delay for 2 seconds so that the program does not run too fast
        time.sleep(1)
        # turn LED0 off
        LED.write(led, led_off)
        # delay for 2 seconds so that the program does not run too fast
        time.sleep(1)