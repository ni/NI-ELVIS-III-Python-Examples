"""
NI ELVIS III Analog Input (AI) 1 sample Example
This example illustrates how to read values from an AI channel on the NI
ELVIS III. To create an AI session, you need to define five parameters: bank,
channel, minvalue, maxvalue, and differential. Bank and channel are required
parameters. The other parameters are optional. The default values of the
optional parameters are:
    range: +/-10
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
    1. Connect a +5V voltage source to AI1 on bank B.
    2. Connect a +3.3V voltage source to AI5 on bank B.

Output:
    The program reads values from AI1 and AI5 on bank B and then return the
    result of AI1 - AI5. The value for AI1 - AI5 is around 1.7.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, AIOChannel, AIMode

# specify the bank, channel and mode for the AI session:
#     bank = B
#     mode = differential
#     channel = AI channel 1 and channel 5 (differential mode)
bank = Bank.B
channel = AIOChannel.AI1
mode = AIMode.DIFFERENTIAL

# open an AI session with differential mode, and set initial values for the
# parameters
with NIELVISIIIAcademicIO.AnalogInput({'bank': bank,
                                       'channel': channel,
                                       'mode': mode}) as AI_single_channel:
    # The program reads values 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # read values from AI1 and AI5
        value_array = AI_single_channel.read()
        # use a loop to print all values
        for value in value_array:
            # the value is around 1.7, respectively
            print value,
        print