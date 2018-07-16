"""
NI ELVIS III Single Point, Multiple Channels, Digital Input and Output Example
This example illustrates how to write values to and read values from multiple
digital input and output (DIO) channel. The program first defines the
configuration for the DIO channels, then reads and writes the DIO channels in
a loop. Each time the write is called a list of data is written to the
channels; each time the read is called a lsit of data is returned for the
channels.

The DIO configuration consists of one parameter: bank. There are two identical
banks of DIO channels (A and B). Each bank contains 19 digital input and
output channels. Each DIO channel contains two directions: write and read. The
NI ELVIS III helper library (academicIO.py) will change the direction based on
the function is called.

Both write and read functions suppport reading/writing multiple channels. To
write to multiple channels, list all the channels after the value_to_write as
indicated in the following line:
    write(value_to_write, channel_to_write_1, channel_to_write_2, ...)
To read from multiple channels as indicated in the following line:
    read(channel_to_read_1, channel_to_read_2, ...)

This example uses:
    1. Bank A, Channel DIO2, write direction.
    2. Bank A, Channel DIO4, read direction.
    3. Bank A, Channel DIO3, write direction.
    4. Bank A, Channel DIO8, read direction.

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
# open a DIO session
with academicIO.DIO(bank) as DIO:
    # specify the DIO channels
    channel2 = DIOChannel.DIO2
    channel3 = DIOChannel.DIO3
    channel4 = DIOChannel.DIO4
    channel8 = DIOChannel.DIO8
    # define the value as a boolean
    value = False

    # write the value False to both DIO2 and DIO3 on bank A
    DIO.write(value, channel2, channel3)
    # read values from DIO4 and DIO8 on bank A
    data = DIO.read(channel4, channel8)
    # the values read are [0, 0]
    print data
