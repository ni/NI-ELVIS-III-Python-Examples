"""
NI ELVIS III Button Example
This example illustrates how to read back the value from the user programmable
button (BUTTON 0) on the NI ELVIS III. The program first defines the
configuration for the button, and then reads from the button registers in a
loop. Each time the read function is called, a Boolean data is returned.
BUTTON 0 is a non-latching push switch. The read function returns True when
the button is pressed and False otherwise. The interval between reads is not
precisely timed, and is controlled by a software delay.

This example uses:
    User programmable button (BUTTON 0).

Hardware setup:
    Press BUTTON 0 on the NI ELVIS III before the program ends.

Result: 
    The program reads back a Boolean value. The value is True when you press
    BUTTON 0, and the program prints a string. Otherwise, the program does
    nothing.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import academicIO

# configure a button session
with academicIO.Button() as button:
    # read values 20 times
    for x in range(0, 20):
        # when you press the button, the if statement is True
        if button.read():
            # print a notice
            print "The Button is pressed."
        # add a short delay before acquiring the next data point
        time.sleep(1)
