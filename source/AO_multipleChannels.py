"""
NI ELVIS III Analog Output (AO) 1 sample Example
This example illustrates how to write value to multiple AO channels on NI
ELVIS III. To create an AO session, you need to define two parameters: bank
and channel. Bank and channel are required parameters.

Output:
    The program writes a value into AO channel 0 and channel 1 on bank A.
    To test the written value, use AI to read the value back. It should be
    approximate to 3.5.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, AIOChannel, AIRange

# specify the analog output bank and channels for the AO session:
#     bank = A
#     channel 0 = AO channel 0
#     channel 1 = AO channel 1
#     range = +/-10
bank = Bank.A
channel0 = AIOChannel.AO0
channel1 = AIOChannel.AO1
airange = AIRange.PLUS_OR_MINUS_10V

# open a AO session with AO channel 0 and channel 1 on bank A, and set the
# initial parameters of the session
with NIELVISIIIAcademicIO.AnalogOutput({'bank': bank,     # define first channel: AO0
                                        'channel': channel0},
                                       {'bank': bank,     # define second channel: AO1
                                        'channel': channel1,
                                        'range': airange}) as AO_multiple_channels:
    # The program writes value 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # a double that is going to be written
        input_value = 3.5
        # write 3.5 into AO0 and AI1 on bank A
        AO_multiple_channels.write(input_value)