"""
NI ELVIS III Analog Input Example - Configuration Options
This example illustrates how to configure and read from the AI channels by
setting different configurations on the NI ELVIS III. The program includes
five different configurations examples. Each time the read function is called,
a single point of data is returned from the channel.

The AI configuration consists of four parameters: bank, channel, range, and
mode. There are two identical banks of AI channels (A and B). Each bank
contains eight analog input channels. Each channel supports four input ranges
(+/-10 V, +/-5 V, +/-2 V, and +/-1 V). Every channel can be configured for
single-ended mode, which references the input to ground. Channels AI0 to AI3
in each bank can be individually configured for differential mode, which
references the selected channel to another channel as indicated in the
following table:
    AI0: AI0 to AI4
    AI1: AI1 to AI5
    AI2: AI2 to AI6
    AI3: AI3 to AI7

The program performs several different acquisitions, each with a different
combination of range and mode.
Section 1 demonstrates the effect of range on the acquisition.
    1. Bank A, Channel AI0, +/-1 V, Single-Ended Mode.
    2. Bank A, Channel AI0, +/-5 V, Single-Ended Mode.
    3. Bank A, Channel AI0, +/-10 V, Single-Ended Mode.
Section 2 demonstrates the effect of mode on the acquisition.
    1. Bank A, Channel AI0, Range +/-10V, Single-Ended Mode.
    2. Bank A, Channel AI1, Range +/-10V, Differential Mode.

Hardware setup:
    1. Connect a +5 V voltage source to AI0 on bank A.
    2. Connect a +3.3 V voltage source to AI1 on bank A.
    3. Connect a +5 V voltage source to AI5 on bank A.

Result:
    Section 1:
        1. Values acquired from AI0 should be around 1 V.
        2. Values acquired from AI0 should be around 5 V.
        3. Values acquired from AI0 should be around 5 V.
    Section 2:
        1. Values acquired from AI0 should be around 5 V.
        2. Values acquired from AI1 and AI5 should be around -1.7 V.
    Expect some small variation due to signal noise.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import academicIO
from enums import Bank, AIChannel, AIRange, AIMode

# specify the bank and channels for the AI sessions
ai_bank = Bank.A
ai_channel0 = AIChannel.AI0
ai_channel1 = AIChannel.AI1

##############################################################################
# Section 1:
# 1. Selecting a smaller range than necessary will clip the signal.
##############################################################################

# specify the range
ai_range = AIRange.PLUS_OR_MINUS_1V
# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel0,
                             'range': ai_range}) as AI_single_channel:
    # read the value
    value_array = AI_single_channel.read()
    # print the value
    print("Range ", ai_range.value, ": ", value_array[0])

##############################################################################
# Section 1:
# 2. Selecting the smallest range that includes your signal for highest
#    measurement resolution.
##############################################################################

# specify the range
ai_range = AIRange.PLUS_OR_MINUS_5V
# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel0,
                             'range': ai_range}) as AI_single_channel:
    # read the value
    value_array = AI_single_channel.read()
    # print the value
    print("Range ", ai_range.value, ": ", value_array[0])

##############################################################################
# Section 1:
# 3. Selecting a larger range than necessary still returns valid data.
##############################################################################

# specify the range
ai_range = AIRange.PLUS_OR_MINUS_10V
# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel0,
                             'range': ai_range}) as AI_single_channel:
    # read the value
    value_array = AI_single_channel.read()
    # print the value
    print("Range ", ai_range.value, ": ", value_array[0])

##############################################################################
# Section 2: 
# 1. Selecting single-ended mode.
##############################################################################

# specify the mode
ai_mode = AIMode.SINGLE_ENDED
# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel0,
                             'mode': ai_mode}) as AI_single_channel:
    # read the value
    value_array = AI_single_channel.read()
    # print the value
    print("Single-Ended: ", value_array[0])

##############################################################################
# Section 2: 
# 2. Selecting differential mode.
##############################################################################

# specify the mode
ai_mode = AIMode.DIFFERENTIAL
# configure the AI channel
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel1,
                             'mode': ai_mode}) as AI_single_channel:
    # read the value
    value_array = AI_single_channel.read()
    # print the value
    print("Differential: ", value_array[0])
