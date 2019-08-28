"""
NI ELVIS III Analog Output Example - Single Point, Multiple Channels
This example illustrates how to write values to multiple analog output (AO)
channels on the NI ELVIS III. The program first defines the configuration for
the AO channels, and then writes to the AO channels in a loop. Each time the
write function is called, a list of single point or multiple points data is written to the
channels. The interval between writes is not precisely timed, and is controlled by
a software delay.

The AO configuration consists of two parameters: bank and channel. There are
two identical banks of AO channels (A and B). Each bank contains two analog
output channels (0 and 1).

A time gap exists between the end of one signal generation and the start of
the next signal generation when you specify n samples (writing multiple
points) mode for Analog Output API. Refer to the following link for more
information about the time gap.
https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md

This example uses:
    1. Bank A, Channel AO0.
    2. Bank A, Channel AO1.

Hardware setup:
    No hardware is needed.

Result:
    The program writes values into both AO0 and AO1 on bank A.
"""
import time
from nielvis import AnalogOutput, Bank, AOChannel

# specify the bank and channels for the AO session
bank = Bank.A
channel0 = AOChannel.AO0
channel1 = AOChannel.AO1

##############################################################################
# Section 1: Single Point (1 Sample)
# Use the write function to write a single point of data to the channel.
# The hardware generates one sample for a channel.
##############################################################################
# configure the AO channels
with AnalogOutput({'bank': bank,     # define first channel: AO0
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

##############################################################################
# Section 2: Multiple Points (N samples)
# Use the write function to write multiple points of data to the channel. The
# hardware generates a finite number of samples for a channel.
##############################################################################
# configure the AO channels
with AnalogOutput({'bank': bank,     # define first channel: AO0
                   'channel': channel0},
                  {'bank': bank,     # define second channel: AO1
                   'channel': channel1}) as AO_multiple_channels:
    # write to the AO channels 20 times
    for i in range(0, 20):
        # define a list of floating-point numbers
        input_value = [1.0, 2.5]
        # specifies the sampling frequency, in hertz, of the output signal.
        sample_rate = 1000
        # write 1.0 and 2.5 to both AO0 and AO1 on bank A
        AO_multiple_channels.write(input_value, sample_rate)

        # add a short delay before writing the next data point
        time.sleep(0.001)
