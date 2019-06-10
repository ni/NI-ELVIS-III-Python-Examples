"""
NI ELVIS III Digital Input and Output Example - Single Point, Multiple Channels
This example illustrates how to write values to and read values from multiple
digital input and output (DIO) channels. The program first defines the
configuration for the DIO channels, and then writes to and reads from the DIO
channels. Each time the write function is called, a data point is written to
the channels; each time the read function is called, a data point is returned
from the channels.

The DIO configuration consists of two parameters: bank and channel. There are
two identical banks of DIO channels (A and B). Each bank contains twenty
digital input and output channels. Each DIO channel contains two directions:
write and read. List all the channels you use, including read and write
channels, in an array when configuring a DIO session. The NI ELVIS III helper
library (academicIO.py) decides the direction based on the function called.

Both the write and the read functions support reading/writing multiple
channels. To write to multiple channels, list all the channels after the value
to write, as indicated in the following line of code:
    write(value_to_write, [channel_to_write_1, channel_to_write_2, ...])
To read from multiple channels, list all the channels to read from, as
indicated in the following line of code:
    read([channel_to_read_1, channel_to_read_2, ...])

This example uses:
    1. Bank A, Channel DIO2, write direction.
    2. Bank A, Channel DIO4, read direction.
    3. Bank A, Channel DIO3, write direction.
    4. Bank A, Channel DIO8, read direction.

Hardware setup:
    1. Connect DIO2 to DIO4 on bank A.
    2. Connect DIO3 to DIO8 on bank A.

Result:
    The program writes values to DIO2 and DIO3 and reads back values from DIO4
    and DIO8 on bank A.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'source/nielvisiii'))

import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank
bank = Bank.A
# specify the DIO channels
channel2 = DIOChannel.DIO2
channel3 = DIOChannel.DIO3
channel4 = DIOChannel.DIO4
channel8 = DIOChannel.DIO8
# configure a DIO session
with academicIO.DigitalInputOutput(bank, [channel2, channel3, channel4, channel8]) as DIO:
    # define the value as a Boolean
    value = False

    # write the value False to both DIO2 and DIO3 on bank A
    # the written value must be a Boolean variable
    DIO.write(value, [channel2, channel3])
    # read values from DIO4 and DIO8 on bank A
    data = DIO.read([channel4, channel8])
    # print the values read. The values read are [0,0]
    print(data)
