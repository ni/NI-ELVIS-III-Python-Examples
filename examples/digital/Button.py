"""
NI ELVIS III Button Example
This example illustrates how to read the value back from the user programmable
button BUTTON 0 on the NI ELVIS III. The program first defines the
configuration for the LED, then reads from the LED registers in a loop. Each
time the read is called a Boolean data is returned. The BUTTON 0 is a
non-latching push switch. The read function returns True when pressed and
False otherwise. The time between reads is not precisely timed, and is
controlled by a software delay.

This example uses:
    User programmable button BUTTON 0.

Hardware setup:
    Press the button BUTTON 0 on NI ELVIS III before the program ends.

Result: 
    The program reads back a Boolean value. The value is True when you press
    the button BUTTON 0, and the program prints a string. Otherwise, do
    nothing.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO

# configure a button session
with academicIO.Button() as button:
    # read values 20 times
    for x in range(0, 20):
        # when you press the button, the if statement is True
        if button.read():
            # print a notice
            print "The Button is pressed."
        # add a short delay before acquiring next data point
        time.sleep(1)
