"""
NI ELVIS III LEDs Example
This example illustrates how to set the states of the LEDs on NI ELVISIII. The
default value for led is set to 'led0'.

Output:
  LED turns on and then turns off.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Led

# open an LEDs session
with NIELVISIIIAcademicIO.LEDs() as LED:
    # specfy the led which to turn on and off
    led = Led.LED0
    # specify statuses
    led_on = True
    led_off = False
    # The program writes value 20 times
    for x in range(0, 20):
        # turn LED0 on
        LED.write(led, led_on)
        # delay for 2 seconds so that the program does not run too fast
        time.sleep(2)
        # turn LED0 off
        LED.write(led, led_off)
        # delay for 2 seconds so that the program does not run too fast
        time.sleep(2)