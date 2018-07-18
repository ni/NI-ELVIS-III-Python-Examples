"""
NI ELVIS III Single Point, Multiple Channels, Analog Input Example
This example illustrates how to read values from multiple analog input (AI)
channels on the NI ELVIS III. The program first defines the configuration for
the AI channels, then reads the AI channels in a loop. Each time the read is
called a list of single point data is returned for the channels. The time
between reads is not precisely timed, and is controlled by a software delay.

The AI configuration consists of four parameters: bank, channel, range, and
mode. There are two identical banks of AI channels (A and B). Each bank
contains 8 analog input channels. Each channel supports four input ranges
(+/-10 V, +/-5 V, +/-2 V, and +/-1 V). Every channel can be configured for
single ended mode, which references the input to ground. Channels AI0 to AI3
in each bank can be individually configured for differential mode, which
references the selected channel to another channel as indicated in this table:
   AI0: AI0 to AI4
   AI1: AI1 to AI5
   AI2: AI2 to AI6
   AI3: AI3 to AI7

This example uses:
    1. Bank A, Channel AI0, Range +/-10 V, Mode Single Ended.
    2. Bank B, Channel AI1, Range +/-5 V, Mode Single Ended.

Hardware setup:
    1. Connect a +5 V voltage source to AI0 on bank A.
    2. Connect a +3.3 V voltage source to AI1 on bank B.

Result:
    Twenty values acquired from each of A/AI0 and B/AI1. All values from A/AI0
    should be around 5 V and from B/AI1 around 3.3 V, expect some small
    variation on each due to signal noise.
"""
import time
import academicIO
from enums import Bank, AIChannel, AIRange, AIMode

# specify the banks, channels, ranges, and mode for the AI session
ai_bankA = Bank.A
ai_bankB = Bank.B
ai_channel0 = AIChannel.AI0
ai_channel1 = AIChannel.AI1
ai_range0 = AIRange.PLUS_OR_MINUS_10V
ai_range1 = AIRange.PLUS_OR_MINUS_5V
ai_mode = AIMode.SINGLE_ENDED

# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bankA,           # define first channel: AI0
                             'channel': ai_channel0,
                             'range': ai_range0,
                             'mode': ai_mode},
                            {'bank': ai_bankB,           # define second channel: AI1
                             'channel': ai_channel1,
                             'range': ai_range1,
                             'mode': ai_mode}) as AI_multiple_channels:
    # read and display the AI channel 20 times
    for i in range(0, 20):
        # read the values
        value_array = AI_multiple_channels.read()
        # use a loop to print all values
        for value in value_array:
            # print the values
            print value

        # add a short delay before acquiring next data point
        time.sleep(0.001)
