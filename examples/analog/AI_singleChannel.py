"""
NI ELVIS III Single Point, Single Channel, Analog Input Example
This example illustrates how to read values from an analog input (AI) channel
on the NI ELVIS III. The program first defines the configuration for the AI
channel, then reads the AI channel in a loop. Each time the read is called a
single point of data is returned for the channel. The time between reads is
not precisely timed, and is controlled by a software delay.

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
    Bank A, Channel AI0, Range +/-10 V, Mode Single Ended.

Hardware setup:
    Connect a +5 V voltage source to AI0 on bank A.

Result:
    Twenty values acquired from AI0. All values should be around 5V, expect
    some small variation due to signal noise.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Bank, AIChannel, AIRange, AIMode

# specify the bank, channel, range, and mode
ai_bank = Bank.A
ai_channel = AIChannel.AI0
ai_range = AIRange.PLUS_OR_MINUS_10V
ai_mode = AIMode.SINGLE_ENDED

# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel,
                             'range': ai_range,
                             'mode': ai_mode}) as AI_single_channel:
    # read and display the AI channel 20 times
    for i in range(0, 20):
        # read the value
        value_array = AI_single_channel.read()
        # print the value
        print value_array[0]

        # add a short delay before acquiring next data point
        time.sleep(0.001)
