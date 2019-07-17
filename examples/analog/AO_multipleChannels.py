"""
NI ELVIS III Analog Output Example - Single Point, Multiple Channels
This example illustrates how to write values to multiple analog output (AO)
channels on the NI ELVIS III. The program first defines the configuration for
the AO channels, and then writes to the AO channels in a loop. Each time the
write function is called, a list of single point data is written to the
channels. The interval between writes is not precisely timed, and is controlled by
a software delay.

The AO configuration consists of two parameters: bank and channel. There are
two identical banks of AO channels (A and B). Each bank contains two analog
output channels (0 and 1).

This example uses:
    1. Bank A, Channel AO0.
    2. Bank A, Channel AO1.

Hardware setup:
    No hardware is needed.

Result:
    The program writes values into both AO0 and AO1 on bank A.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import academicIO
from enums import Bank, AOChannel

# specify the bank and channels for the AO session
bank = Bank.A
channel0 = AOChannel.AO0
channel1 = AOChannel.AO1

# configure the AO channels
with academicIO.AnalogOutput({'bank': bank,     # define first channel: AO0
                              'channel': channel0},
                             {'bank': bank,     # define second channel: AO1
                              'channel': channel1}) as AO_multiple_channels:
    # write to the AO channels 20 times
    for i in range(0, 20):
        # define the value as a floating-point number
        input_value = 3.5
        # write 3.5 to both AO0 and AO1 on bank A
        AO_multiple_channels.write(input_value)

        # add a short delay before writing the next data point
        time.sleep(0.001)
