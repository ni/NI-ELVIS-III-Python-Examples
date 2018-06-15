"""
NI ELVIS III Analog Input (AI) 1 Sample Example - Multiple Channels
This example illustrates how to read values from the multiple AI channels on
the NI ELVIS III. To create an AI session, you need to define five parameters:
bank, channel, minvalue, maxvalue, and differential. Bank and channel are
required parameters. The other parameters are optional. The default values of
the optional parameters are:
    minvalue: -10
    maxvalue: 10
    differential: False

You use the AI differential mode to acquire the difference between two AI
channels. To turn on the differential mode, specify differential as True. The
channels available in the AI differential mode and the channels they compare
are:
    channel: 0  ->  AI 0 minus AI 4
    channel: 1  ->  AI 1 minus AI 5
    channel: 2  ->  AI 2 minus AI 6
    channel: 3  ->  AI 3 minus AI 7

Hardware setup:
    1. Connect a +5V voltage source to AI0 on bank A.
    2. Connect a +3.3V voltage source to AI1 on bank A.

Output:
    The program reads values from AI0 and AI1 on bank A.
    The value for AI0 is around 5.0.
    The value for AI1 is around 3.3.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, AIOChannel, AIRange, AIMode

# specify the bank, channel, minvale, maxvalue, and mode for the AI session:
#     bank = A
#     channel 0 = AI channel 0
#     channel 1 = AI channel 1
#     minvalue = -10
#     maxvalue = 10
#     mode = none differential mode
bank = Bank.A
channel0 = AIOChannel.AI0
channel1 = AIOChannel.AI1
ai_range = AIRange.PLUS_OR_MINUS_10V
mode = AIMode.NONE

# open an AI session, and set initial values for the parameters
with NIELVISIIIAcademicIO.AnalogInput({'bank': bank,           # define first channel: AI0
                                       'channel': channel0,
                                       'range': ai_range,
                                       'mode': mode},
                                      {'bank': bank,           # define second channel: AI1
                                       'channel': channel1,
                                       'mode': mode}) as AI_multiple_channels:
    # The program reads values 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # read values from AI0 and AI1
        value_array = AI_multiple_channels.read()
        # use a loop to print all values
        for value in value_array:
            # the values are around 5.0 and 3.3 on the two channels, respectively
            print value,
        print