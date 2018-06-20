"""
NI ELVIS III Analog Input (AI) 1 sample Example - Single Channel
This example illustrates how to read values from an AI channel on the NI ELVIS
III. It uses channel AI2 on Bank B with range +/-10 V under Single Ended Mode.
Each time the read() is called, a single point of data is returned from the
channel. The time between reads is not precisely timed, and is controlled by a
software delay.

To create an AI session, you need to define four parameters: bank, channel,
range, and mode. bank and channel are required parameters. The other
parameters are optional. The default values of the optional parameters are:
    range = PLUS_OR_MINUS_10V 
    mode = SINGLE_ENDED

You use the AI differential mode to acquire the difference between two AI
channels. To turn on the differential mode, specify AIMode as DIFFERENTIAL.
The channels available in the AI differential mode and the channels they
compare are:
    AIOChannel.AI0  ->  AI0 minus AI4
    AIOChannel.AI1  ->  AI1 minus AI5
    AIOChannel.AI2  ->  AI2 minus AI6
    AIOChannel.AI3  ->  AI3 minus AI7

Hardware setup:
    Connect a +5 V voltage source to AI2 on bank B.

Result:
    The program reads values from AI2 on bank B.
"""
import time
import academicIO
from enums import Bank, AIOChannel, AIRange, AIMode

# specify the bank, channel and mode for the AI session
bank = Bank.B
channel = AIOChannel.AI2
range10V = AIRange.PLUS_OR_MINUS_10V
mode = AIMode.SINGLE_ENDED

# open an AI session, and set initial values for the parameters
with academicIO.AnalogInput({'bank': bank,
                             'channel': channel,
                             'range': range10V,
                             'mode': mode}) as AI_single_channel:
    # The program reads values 20 times
    for i in range(0, 20):
        # read value from AI2
        value_array = AI_single_channel.read()
        # the value is around 5
        print value_array[0]

        # add a short delay before acquiring next data point
        time.sleep(0.001)
