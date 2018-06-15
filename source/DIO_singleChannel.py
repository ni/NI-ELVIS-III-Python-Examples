"""
NI ELVIS III DIO Example
This example illustrates how to write value to and read value from one digital
input and output channel. To create a DIO session, you need to define one
parameter: bank. The default value of bank is bank A.

Hardware setup:
    1. Connect DIO2 to DIO4 on bank A.

Output:
    The program reads values from DIO4 on bank A.
    The value is [0].
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, DIOChannel

# specify the digital input and output bank from which to read and write the
# value
bank = Bank.A
# open a DIO session, and set the initial parameters
with NIELVISIIIAcademicIO.DIO(bank) as DIO:
    # specify the digital input and output channel from which to read and
    # write the value
    channel2 = DIOChannel.DIO2
    channel4 = DIOChannel.DIO4
    # specify the input value
    value = False
    # The program reads values 20 times
    for x in range(0, 20):
        # write False to DIO2 on bank A
        DIO.write(value, channel2)
        # read value from DIO4 on bank A
        data = DIO.read(channel4)
        # the value is [0]
        print data

        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)