"""
NI ELVIS III Single Point, Multiple Channels, Digital Input and Output Example
This example illustrates how to write values to and read values from multiple
digital input and output (DIO) channel. The program first defines the
configuration for the DIO channels, then reads and writes the DIO channels in
a loop. Each time the write is called a list of data is written to the
channels; each time the read is called a lsit of data is returned for the
channels. The time between writes and reads is not precisely timed and is
controlled by a software delay.

The DIO configuration consists of one parameter: bank. There are two identical
banks of DIO channels (A and B). Each bank contains 19 digital input and
output channels. Each DIO channel contains two directions: write and read. The
NI ELVIS III helper library (academicIO.py) will change the direction based on
the function is called.

This example uses:
    Bank A, Channel DIO2, write direction.
    Bank A, Channel DIO4, read direction.
    Bank A, Channel DIO3, write direction.
    Bank A, Channel DIO8, read direction.

Hardware setup:
    1. Connect DIO2 to DIO4 on bank A.
    2. Connect DIO3 to DIO8 on bank A.

Result:
    The program writes values to DIO2 and DIO3 and reads values from DIO4 and
    DIO8 on bank A.
"""
import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank
bank = Bank.A
# open a DIO session, and set the initial values for the parameters
with academicIO.DIO(bank) as DIO:
    # specify the DIO channels
    channel2 = DIOChannel.DIO2
    channel3 = DIOChannel.DIO3
    channel4 = DIOChannel.DIO4
    channel8 = DIOChannel.DIO8
    # define the value as a boolean
    value = False
    # writes to and reads from the DIO channels 20 times
    for x in range(0, 20):
        # write the value False to both DIO2 and DIO3 on bank A
        DIO.write(value, channel2, channel3)
        # read values from DIO4 and DIO8 on bank A
        data = DIO.read(channel4, channel8)
        # the values read are [0, 0]
        print data

        # add a short delay before acquiring next data point
        time.sleep(0.001)