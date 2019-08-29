"""
NI ELVIS III Analog Output Example - Single Point, Single Channel
This example illustrates how to write values to an analog output (AO)
channel on the NI ELVIS III. The program first defines the configuration for
the AO channel, and then writes to the AO channel in a loop. Each time the
write function is called, a single point or multiple points of data is written to the channel.
The interval between writes is not precisely timed, and is controlled by a
software delay.

The AO configuration consists of two parameters: bank and channel. There are
two identical banks of AO channels (A and B). Each bank contains two analog
output channels (0 and 1).

A time gap exists between the end of one signal generates and the start of
the next signal generates when you specify n samples (writing multiple
points) mode for Analog Output API. Refer to the following link for more
information about the time gap.
https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md

This example uses:
    Bank A, Channel AO0.

Hardware setup:
    No hardware is needed.

Result:
    The program writes values to AO0 on bank A.
"""
import time
from nielvis import AnalogOutput, Bank, AOChannel

# specify the bank and channel for the AO session
bank = Bank.A
channel = AOChannel.AO0

##############################################################################
# Section 1: Single Point (1 Sample)
# Use the write function to write a single point of data to the channel.
# The hardware generates one sample for a channel.
##############################################################################
# configure the AO channel
with AnalogOutput({'bank': bank,
                   'channel': channel}) as AO_single_channel:

    # write to the AO channel 20 times
    for i in range(0, 20):
        # define the value as a floating-point number
        input_value = 2.0
        # write 2.0 to AO0 on bank A
        AO_single_channel.write(input_value)

        # add a short delay before writing the next data point
        time.sleep(0.001)

##############################################################################
# Section 2: Multiple Points (N samples)
# Use the write function to write multiple points of data to the channel. The
# hardware generates a finite number of samples for a channel.
##############################################################################
# configure the AO channel
with AnalogOutput({'bank': bank,
                   'channel': channel}) as AO_single_channel:

    # write to the AO channel 20 times
    for i in range(0, 20):
        # define a list of floating-point numbers
        input_value = [1.0, 2.5]
        # specifies the sampling frequency, in hertz, of the output signal.
        sample_rate = 1000
        # write 1.0 and 2.5 to both AO0 and AO1 on bank A
        AO_single_channel.write(input_value, sample_rate)

        # add a short delay before writing the next data point
        time.sleep(0.001)
