"""
NI ELVIS III Analog Input Example - Multiple Channels
This example illustrates how to read values from multiple analog input (AI)
channels on the NI ELVIS III. The program first defines the configuration for
the AI channels, and then reads the AI channels in a loop. Each time the read
function is called, a list of single point or multiple points data is returned
for the channels. The interval between reads is not precisely timed, and is
controlled by a software delay.

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

A time gap exists between the end of one signal acquisition and the start of
the next signal acquisition when you specify N sample (reading multiple
points) mode for Analog Input API. Refers to the following link for more
information about the time gap.
https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/NI_ELVIS_III_Understanding_Gaps.md

This example uses:
    1. Bank A, Channel AI0, Range +/-10 V, Single-Ended Mode.
    2. Bank B, Channel AI1, Range +/-5 V, Single-Ended Mode.

Hardware setup:
    1. Connect a +5 V voltage source to AI0 on bank A.
    2. Connect a +3.3 V voltage source to AI1 on bank B.

Result:
    Twenty values are acquired from both A/AI0 and B/AI1. All values from
    A/AI0 should be around 5 V, and all values from B/AI1 should be around
    3.3 V. Expect some small variation due to signal noise.
"""
import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

# specify the banks, channels, ranges, and mode for the AI session
ai_bankA = Bank.A
ai_bankB = Bank.B
ai_channel0 = AIChannel.AI0
ai_channel1 = AIChannel.AI1
ai_range0 = AIRange.PLUS_OR_MINUS_10V
ai_range1 = AIRange.PLUS_OR_MINUS_5V
ai_mode = AIMode.SINGLE_ENDED

##############################################################################
# Section 1: Single Point (1 Sample)
# Use the read function to read a single point of data back from the channel.
# The hardware acquires one sample for a channel.
##############################################################################
print('Single Point, Multiple Channels')
# configure the AI channel
with AnalogInput({'bank': ai_bankA,           # define the first channel: AI0
                  'channel': ai_channel0,
                  'range': ai_range0,
                  'mode': ai_mode},
                 {'bank': ai_bankB,           # define the second channel: AI1
                  'channel': ai_channel1,
                  'range': ai_range1,
                  'mode': ai_mode}) as AI_multiple_channels:
    # read from the AI channels and display the values 20 times
    for i in range(0, 20):
        # read the values
        value_array = AI_multiple_channels.read()
        # use a loop to print all values
        for value in value_array:
            # print the values
            print(value)

        # add a short delay before acquiring the next data point
        time.sleep(0.001)

##############################################################################
# Section 2: Multiple Points (N sample)
# Use the read function to read multiple points of data from the channel. The
# hardware acquires a finite number of samples for a channel.
##############################################################################
print('Multiple Points, Multiple Channels')
# configure the AI channel
with AnalogInput({'bank': ai_bankA,           # define the first channel: AI0
                  'channel': ai_channel0,
                  'range': ai_range0,
                  'mode': ai_mode},
                 {'bank': ai_bankB,           # define the second channel: AI1
                  'channel': ai_channel1,
                  'range': ai_range1,
                  'mode': ai_mode}) as AI_multiple_channels:
    # specify the number of samples to read and the sampling frequency, in
    # hertz, of the input signal
    number_of_samples = 100
    sample_rate = 1000
    # read from the AI channel and display the values 20 times
    for i in range(0, 20):
        # read the value
        value_array = AI_multiple_channels.read(number_of_samples, sample_rate)

        # print the Bank A value
        print('Bank A:')
        for value in value_array[0]:
            print(value)
        # print the Bank B value
        print('Bank B:')
        for value in value_array[1]:
            print(value)

        # add a short delay before acquiring the next data point
        time.sleep(0.001)
