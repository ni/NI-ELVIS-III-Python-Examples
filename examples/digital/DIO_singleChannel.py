"""
NI ELVIS III Single Point, Single Channel, Digital Input and Output Example
This example illustrates how to write a value to and read a value from a single
digital input and output (DIO) channel. The program first defines the
configuration for the DIO channels, then writes to and reads from the DIO
channels. Each time the write is called a data is written to the channel; each
time the read is called a data is returned for the channel.

The DIO configuration consists of one parameter: bank. There are two identical
banks of DIO channels (A and B). Each bank contains 19 digital input and
output channels. Each DIO channel contains two directions: write and read. The
NI ELVIS III helper library (academicIO.py) will change the direction based on
the function is called.

This example uses:
    1. Bank A, Channel DIO2, write direction.
    2. Bank A, Channel DIO4, read direction.

Hardware setup:
    Connect DIO2 to DIO4 on bank A.

Result:
    The program writes a value to DIO2 and reads back a value from DIO4 on
    bank A.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Bank, DIOChannel

# specify the bank
bank = Bank.A
# configure a DIO session
with academicIO.DigitalInputOutput(bank) as DIO:
    # specify the DIO channels
    channel2 = DIOChannel.DIO2
    channel4 = DIOChannel.DIO4
    # define the value as a boolean
    value = True

    # write the value True to DIO2 on bank A
    # the written value must be a boolean variable
    DIO.write(value, channel2)
    # read value from DIO4 on bank A
    data = DIO.read(channel4)
    # the value read is [1]
    print data
