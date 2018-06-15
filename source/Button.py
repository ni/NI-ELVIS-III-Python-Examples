"""
NI ELVIS III Button Example
This example illustrates how to button on NI ELVIS III.

Output:
    A string is printed when the button is clicked.
"""
import time
import NIELVISIIIAcademicIO

# open an Button session
with NIELVISIIIAcademicIO.Button() as button:
    # The program reads values 20 times
    for x in range(0, 20):
        # print number of loop counts
        print "loop ", x
        # if the button is clicked
        if button.read():
            # print a notice
            print "The Button is clicked."
        # delay for 0.1 seconds so that the program does not run too fast
        time.sleep(1)