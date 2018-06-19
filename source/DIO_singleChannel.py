"""
NI ELVIS III Digital Input and Output (DIO) Example - Single Channel
This example illustrates how to write values to and read values from a single
digital input and output channel. To create a DIO session, you need to define
bank, which is an optional parameter. The default value of bank is A.

Hardware setup:
    Connect DIO2 to DIO4 on bank A.

Result:
    The program writes values to DIO2 and reads values from DIO4 on bank A.
"""
import time
import academicIO
from enums import Bank, DIOChannel

# specify the bank
bank = Bank.A
# open a DIO session, and set the initial values for the parameters
with academicIO.DIO(bank) as DIO:
    # specify the DIO channels
    channel2 = DIOChannel.DIO2
    channel4 = DIOChannel.DIO4
    # specify the input value
    value = True
    # The program generates and reads values 20 times
    for x in range(0, 20):
        # write value to DIO2 on bank A
        DIO.write(value, channel2)
        # read value from DIO4 on bank A
        data = DIO.read(channel4)
        # the value read is [0]
        print data

        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)