"""
NI ELVIS III Digital Input and Output Example - Single Point, Single Channel, 
This example illustrates how to write a value to and read a value from a single
digital input and output (DIO) channel. The program first defines the
configuration for the DIO channel, and then writes to and reads from the DIO
channels. Each time the write function is called, a data point is written to
the channel; each time the read function is called, a data point is returned
for the channel.

The DIO configuration consists of two parameters: bank and channel. There are
two identical banks of DIO channels (A and B). Each bank contains twenty
digital input and output channels. Each DIO channel contains two directions:
write and read. List all the channels you use, including read and write
channels, in an array when configuring a DIO session. The NI ELVIS III helper
library (academicIO.py) decides the direction based on the function called.

This example uses:
    1. Bank A, Channel DIO2, write direction.
    2. Bank A, Channel DIO4, read direction.

Hardware setup:
    Connect DIO2 to DIO4 on bank A.

Result:
    The program writes a value to DIO2 and reads back a value from DIO4 on
    bank A.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank
bank = Bank.A
# specify the DIO channels
channel2 = DIOChannel.DIO2
channel4 = DIOChannel.DIO4
# configure a DIO session
with academicIO.DigitalInputOutput(bank, [channel2, channel4]) as DIO:
    # define the value as a Boolean
    value = True

    # write the value True to DIO2 on bank A
    # the written value must be a Boolean variable
    DIO.write(value, [channel2])
    # read value from DIO4 on bank A
    data = DIO.read([channel4])
    # the value read is [1]
    print data
