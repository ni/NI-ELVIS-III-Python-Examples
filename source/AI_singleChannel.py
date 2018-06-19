"""
NI ELVIS III Analog Input (AI) 1 sample Example - Single Channel
This example illustrates how to read values from an AI channel on the NI
ELVIS III. To create an AI session, you need to define four parameters: bank,
channel, range, and mode. bank and channel are required parameters. The other
parameters are optional. The default values of the optional parameters are:
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
    1. Connect a +5 V voltage source to AI1 on bank B.
    2. Connect a +3.3 V voltage source to AI5 on bank B.

Result:
    The program reads values from AI1 and AI5 on bank B and then returns the
    result of AI1 - AI5.
"""
import time
import academicIO
from enums import Bank, AIOChannel, AIMode

# specify the bank, channel and mode for the AI session
# AI1 represents AI1 - AI5 in differential mode
bank = Bank.B
channel = AIOChannel.AI1
mode = AIMode.DIFFERENTIAL

# open an AI session, and set initial values for the parameters
with academicIO.AnalogInput({'bank': bank,
                             'channel': channel,
                             'mode': mode}) as AI_single_channel:
    # The program reads values 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # read the diff values from AI1 and AI5
        value_array = AI_single_channel.read()
        # the value is around 1.7
        print value_array[0]