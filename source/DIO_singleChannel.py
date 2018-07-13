"""
NI ELVIS III Single Point, Single Channel, Digital Input and Output Example
This example illustrates how to write values to and read values from a single
digital input and output (DIO) channel. The program first defines the
configuration for the DIO channels, then reads and writes the DIO channel in a
loop. Each time the write is called a data is written to the channel; each
time the read is called a data is returned for the channel. The time between
reads is not precisely timed and is controlled by a software delay.

The DIO configuration consists of one parameter: bank. There are two identical
banks of DIO channels (A and B). Each bank contains 19 digital input and
output channels. Each DIO channel contains two directions: write and read. The
NI ELVIS III helper library (academicIO.py) will change the direction based on
the function is called.

This example uses:
    Bank A, Channel DIO2, write direction.
    Bank A, Channel DIO4, read direction.

Hardware setup:
    Connect DIO2 to DIO4 on bank A.

Result:
    The program writes values to DIO2 and reads values from DIO4 on bank A.
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
    channel4 = DIOChannel.DIO4
    # define the value as a boolean
    value = True
    # writes to and reads from the DIO channels 20 times
    for x in range(0, 20):
        # write the value True to DIO2 on bank A
        DIO.write(value, channel2)
        # read value from DIO4 on bank A
        data = DIO.read(channel4)
        # the value read is [1]
        print data

        # add a short delay before acquiring next data point
        time.sleep(0.001)