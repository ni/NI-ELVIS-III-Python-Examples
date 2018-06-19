"""
NI ELVIS III Analog Input (AI) 1 Sample Example - Multiple Channels
This example illustrates how to read values from multiple AI channels on the
NI ELVIS III. To create an AI session, you need to define four parameters:
bank, channel, range, and mode. bank and channel are required parameters. The
other parameters are optional. The default values of the optional parameters
are:
    range = PLUS_OR_MINUS_10V 
    mode = NONE

You use the AI differential mode to acquire the difference between two AI
channels. To turn on the differential mode, specify AIMode as DIFFERENTIAL.
The channels available in the AI differential mode and the channels they
compare are:
    AIOChannel.AI0  ->  AI0 minus AI4
    AIOChannel.AI1  ->  AI1 minus AI5
    AIOChannel.AI2  ->  AI2 minus AI6
    AIOChannel.AI3  ->  AI3 minus AI7

Hardware setup:
    1. Connect a +5 V voltage source to AI0 on bank A.
    2. Connect a +3.3 V voltage source to AI1 on bank A.

Output:
    The program reads values from AI0 and AI1 on bank A.
"""
import time
import academicIO
from enums import Bank, AIOChannel, AIRange, AIMode

# specify the bank, channels, range, and mode for the AI session
bank = Bank.A
channel0 = AIOChannel.AI0
channel1 = AIOChannel.AI1
ai_range = AIRange.PLUS_OR_MINUS_10V
mode = AIMode.NONE

# open an AI session, and set initial values for the parameters
with academicIO.AnalogInput({'bank': bank,           # define first channel: AI0
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
            # the values read are around 5.0 and 3.3 on the two channels, respectively
            print value