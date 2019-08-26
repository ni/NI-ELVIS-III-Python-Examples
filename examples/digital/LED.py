"""
NI ELVIS III LED Example
This example illustrates how to set the status of the LEDs on the NI ELVIS III.
The program first defines the configuration for the LED session, and then writes
to the LED register in a loop. Each time the write function is called a
Boolean data is written to the register. The time between reads is not
precisely timed, and is controlled by a software delay.

This example uses:
    LED0.

Hardware setup:
    No hardware is needed.

Result:
    LED0 flashes for 5 seconds.
"""
import time
from nielvis import LEDs, Led

# configure an LED session
with LEDs() as LED:
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True
    # writes values 10 times, which makes LED0 flash for 5 seconds
    for x in range(0, 10):
        # turn LED0 on or off
        # the first parameter of the write function specifies which LED to
        # write to. The second parameter specifies the status of the LED, which
        # should be either True or False
        LED.write(led, led_on_off)
        # add a short delay
        time.sleep(0.5)
        # if the LED is on, set the parameter to off
        # if the LED is off, set the parameter to on
        led_on_off = not led_on_off