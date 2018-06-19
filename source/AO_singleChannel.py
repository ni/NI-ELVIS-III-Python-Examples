"""
NI ELVIS III Analog Output (AO) 1 Sample Example - Single Channel
This example illustrates how to write values to an AO channel on the NI ELVIS
III. To create an AO session, you need to define two parameters: bank and
channel. Both are required parameters.

Result:
    The program writes values to AO0 on bank A.
"""
import time
import academicIO
from enums import Bank, AIOChannel

# specify the bank, channel for the AO session
bank = Bank.A
channel = AIOChannel.AO0

# open an AO session and set the initial values for the parameters
with academicIO.AnalogOutput({'bank': bank,
                                        'channel': channel}) as AO_single_channel:

    # The program writes values 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # define the value as a floating-point number
        input_value = 2.0
        # write 2.0 to AO0 on bank A
        AO_single_channel.write(input_value)