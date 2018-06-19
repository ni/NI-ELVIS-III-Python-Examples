"""
NI ELVIS III Button Example
This example illustrates how to read the value from the user programmable
button BUTTON 0 on the NI ELVIS III. The BUTTON 0 is a non-latching push
switch. It returns True when pressed and False otherwise.

Result: 
    The program prints a string when you press the button.
"""
import time
import academicIO

# open a button session
with academicIO.Button() as button:
    # The program reads values 20 times
    for x in range(0, 20):
        # print the loop count
        print "loop ", x
        # when you press the button, the if statement is True
        if button.read():
            # print a notice
            print "The Button is pressed."
        # delay for 0.1 seconds so that the program does not run too fast
        time.sleep(1)