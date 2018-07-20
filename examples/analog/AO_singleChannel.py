"""
NI ELVIS III Single Point, Single Channel, Analog Output Example
This example illustrates how to write values to an analog output (AO)
channel on the NI ELVIS III. The program first defines the configuration for
the AO channel, then writes to the AO channel in a loop. Each time the write
is called a single point of data is written to the channel. The time between
writes is not precisely timed, and is controlled by a software delay.

The AO configuration consists of two parameters: bank and channel. There are
two identical banks of AO channels (A and B). Each bank contains 2 analog
output channels. Every channel can be configured for single ended mode.

This example uses:
    Bank A, Channel AI0.

Hardware setup:
    No hardware is needed.

Result:
    The program writes values to AO0 on bank A.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Bank, AOChannel

# specify the bank, channel for the AO session
bank = Bank.A
channel = AOChannel.AO0

# configure the AO channel
with academicIO.AnalogOutput({'bank': bank,
                              'channel': channel}) as AO_single_channel:

    # write to the AO channel 20 times
    for i in range(0, 20):
        # define the value as a floating-point number
        input_value = 2.0
        # write 2.0 to AO0 on bank A
        AO_single_channel.write(input_value)

        # add a short delay before acquiring next data point
        time.sleep(0.001)
