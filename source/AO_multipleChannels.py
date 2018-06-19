"""
NI ELVIS III Analog Output (AO) 1 Sample Example - Multiple Channels
This example illustrates how to write values to multiple AO channels on the NI
ELVIS III. To create an AO session, you need to define two parameters: bank
and channel. Both are required parameters.

Result:
    The program writes a values into both AO0 and AO1 on bank A.
"""
import time
import academicIO
from enums import Bank, AIOChannel, AIRange

# specify the bank, channels, and range for the AO session
bank = Bank.A
channel0 = AIOChannel.AO0
channel1 = AIOChannel.AO1
airange = AIRange.PLUS_OR_MINUS_10V

# open an AO session and set the initial values for the parameters
with academicIO.AnalogOutput({'bank': bank,     # define first channel: AO0
                                        'channel': channel0},
                                       {'bank': bank,     # define second channel: AO1
                                        'channel': channel1,
                                        'range': airange}) as AO_multiple_channels:
    # The program writes values 20 times
    for i in range(0, 20):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # define the value as a floating-point number
        input_value = 3.5
        # write 3.5 to both AO0 and AI1 on bank A
        AO_multiple_channels.write(input_value)