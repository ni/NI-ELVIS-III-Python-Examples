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

You can use the Python ELVIS III Analog Output APIs to perform signal
generation in three I/O modes: 1 sample, n samples, and continuous. Refer to
the following link to understand the differences among 1 sample, n samples,
and continuous modes.
https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/1_Sample_N_Samples_and_Continuous_Modes.md

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
# Use the write function to write a single point of data to the channels.
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
# Section 2: Multiple Points (n samples)
# Use the write function to write multiple points of data to the channels. The
# hardware generates a finite number of samples for a channel.

# A time gap exists between the end of one signal generation and the start of
# the next signal generation when you specify n samples mode (writing
# multiple points) for Analog Output API. Refer to the following link for more
# information about the time gap.
# https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md
#
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
        # specify the sampling frequency, in hertz, of the output signal.
        sample_rate = 1000
        # write 1.0 and 2.5 to both AO0 and AO1 on bank A
        AO_multiple_channels.write(input_value, sample_rate)

        # add a short delay before writing the next data point
        time.sleep(0.001)

##############################################################################
# Section 3: Multiple Points (continuous)
# Use the start_continuous_mode, write, and stop_continuous_mode functions to
# write multiple points of data to the channels. The hardware continuously
# generates samples for a channel until the generation is stopped.
##############################################################################
# configure the AO channels
with AnalogOutput({'bank': bank,     # define first channel: AO0
                   'channel': channel0},
                  {'bank': bank,     # define second channel: AO1
                   'channel': channel1}) as AO_multiple_channels:
    # define a list of floating-point numbers, the input value should be
    # defined in the format: [[values_for_first_channel],
    # [values_for_second_channel], ...]
    input_values = [[1.0, 2.0, 3.0, 4.0, 5.0], [5.0, 4.0, 3.0, 2.0, 1.0]]
    # specify the sampling frequency, in hertz, of the output signal
    sample_rate = 1000
    # specify the period of time, in milliseconds, to wait for pushing the
    # remaining data to the buffer when the size of the remaining data is
    # larger than the remaining buffer
    timeout = -1

    # configure the sample rate and timeout, then starts the signal generation
    AO_multiple_channels.start_continuous_mode(input_values, sample_rate, timeout)

    # write to the AO channels 20 times
    for i in range(0, 20):
        # write [1.0, 2.0, 3.0, 4.0, 5.0] to AO0 on bank A
        # write [5.0, 4.0, 3.0, 2.0, 1.0] to AO1 on bank A
        AO_multiple_channels.write(input_values, sample_rate)
    
    # stop signal generation
    AO_multiple_channels.stop_continuous_mode()
