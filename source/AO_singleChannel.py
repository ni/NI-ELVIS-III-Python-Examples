"""
NI ELVIS III Analog Output (AO) 1 sample Example
This example illustrates how to write value to an AO channel on NI ELVIS III.
To create an AO session, you need to define two parameters: bank and channel.
Bank and channel are required parameters.

Output:
    The program writes a value into AO channel 0 on bank A.
    To test the written value, use AI to read the value back. It should be
    approximate to 2.0.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, AIOChannel

# specify the analog output bank and channel for the AO session:
#     bank = A
#     channel 0 = AO channel 0
bank = Bank.A
channel = AIOChannel.AO0

# open a AO session with AO channel 0 on bank A, and set the initial
# parameters of the session
with NIELVISIIIAcademicIO.AnalogOutput({'bank': bank,
                                        'channel': channel}) as AO_single_channel:

    # The program writes value 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # a double that is going to be written
        input_value = 2.0
        # write 2.0 into AO0
        AO_single_channel.write(input_value)