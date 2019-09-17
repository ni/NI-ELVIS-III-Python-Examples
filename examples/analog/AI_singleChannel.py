"""
NI ELVIS III Analog Input Example - Single Channel
This example illustrates how to read values from an analog input (AI) channel
on the NI ELVIS III. The program first defines the configuration for the AI
channel, and then reads the AI channel in a loop. Each time the read function
is called, a single point or multiple points of data is returned for the
channel. The interval between reads is not precisely timed, and is controlled
by a software delay.

The AI configuration consists of four parameters: bank, channel, range, and
mode. There are two identical banks of AI channels (A and B). Each bank
contains eight analog input channels. Each channel supports four input ranges
(+/-10 V, +/-5 V, +/-2 V, and +/-1 V). Every channel can be configured for
single-ended mode, which references the input to ground. Channels AI0 to AI3
in each bank can be individually configured for differential mode, which
references the selected channel to another channel as indicated in this table:
   AI0: AI0 to AI4
   AI1: AI1 to AI5
   AI2: AI2 to AI6
   AI3: AI3 to AI7

You can use the Python ELVIS III Analog Input APIs to perform signal
acquisition in three I/O modes: 1 sample, n samples, and continuous. Refer to
the following link to understand the differences among 1 sample, n samples,
and continuous modes.
https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/1_Sample_N_Samples_and_Continuous_Modes.md

This example uses:
    Bank A, Channel AI0, Range +/-10 V, Single-Ended Mode.

Hardware setup:
    Connect a +5 V voltage source to AI0 on bank A.

Result:
    Twenty values are acquired from AI0. All values should be around 5V.
    Expect some small variation due to signal noise.
"""
import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

# specify the bank, channel, range, and mode
ai_bank = Bank.A
ai_channel = AIChannel.AI0
ai_range = AIRange.PLUS_OR_MINUS_10V
ai_mode = AIMode.SINGLE_ENDED

##############################################################################
# Section 1: Single Point (1 Sample)
# Use the read function to read a single point of data back from the channel. The
# hardware acquires one sample for a channel.
##############################################################################
print('Single Point, Single Channel')
# configure the AI channel
with AnalogInput({'bank': ai_bank,
                  'channel': ai_channel,
                  'range': ai_range,
                  'mode': ai_mode}) as AI_single_channel:
    # read from the AI channel and display the values 20 times
    for i in range(0, 20):
        # read the value
        value_array = AI_single_channel.read()
        # print the value
        print(value_array[0])

        # add a short delay before acquiring the next data point
        time.sleep(0.001)

##############################################################################
# Section 2: Multiple Points (n samples)
# Use the read function to read multiple points of data from the channel. The
# hardware acquires a finite number of samples for a channel.
#
# A time gap exists between the end of one signal acquisition and the start of
# the next signal acquisition when you specify n samples mode (reading
# multiple points) for Analog Input API. Refer to the following link for more
# information about the time gap.
# https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md
#
##############################################################################
print('Multiple Points, Single Channel (n samples)')
# configure the AI channel
with AnalogInput({'bank': ai_bank,
                  'channel': ai_channel,
                  'range': ai_range,
                  'mode': ai_mode}) as AI_single_channel:
    # specify the number of samples to read and the sampling frequency, in
    # hertz, of the input signal
    number_of_samples = 100
    sample_rate = 1000
    # read from the AI channel and display the values 20 times
    for i in range(0, 20):
        # read the value
        value_array = AI_single_channel.read(number_of_samples, sample_rate)

        # print the value
        for value in value_array[0]:
            print(value)

        # add a short delay before acquiring the next data point
        time.sleep(0.001)

##############################################################################
# Section 3: Multiple Points (continuous)
# Use the start_continuous_mode, read, and stop_continuous_mode functions to
# read multiple points of data from the channel. The hardware continuously
# acquires samples for a channel until the acquisition is stopped.
##############################################################################
print('Multiple Points, Single Channel (continuous)')
# configure the AI channel
with AnalogInput({'bank': ai_bank,
                  'channel': ai_channel,
                  'range': ai_range,
                  'mode': ai_mode}) as AI_single_channel:
    # specify the number of samples to read and the sampling frequency, in
    # hertz, of the input signal
    number_of_samples = 100
    sample_rate = 1000
    # specify the period of time, in milliseconds, to wait for the acquisition
    # to complete
    timeout = -1
    
    # configure the sample rate and start the acquisition
    AI_single_channel.start_continuous_mode(sample_rate)
    
    # read from the AI channel and display the values 20 times
    for i in range(0, 20):
        # read the value
        value_array = AI_single_channel.read(number_of_samples, timeout)

        # print the value
        for value in value_array[0]:
            print(value)

    # stop signal acquisition
    AI_single_channel.stop_continuous_mode()
