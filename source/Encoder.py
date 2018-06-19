"""
NI ELVIS III Encoder Example
This example illustrates how to read and decode signals from an encoder
through the encoder channels on the NI ELVIS III. To create an encoder session,
you need to define three parameters: bank, channel and mode. mode is an
optional parameter. The default value of mode is QUADRATURE. To read and
decode signals from the encoder device, you need to define one parameter,
reset_counter. The default value of reset_counter is False.

Hardware setup:
	1. Connect phase A (default is DIO0) on bank A to ENC.A of a encoder
       device.
	2. Connect phase B (default is DIO1) on bank A to ENC.B of a encoder
       device.

Result:
	The program reads the counter value and the counter direction from the
    encoder device.
"""
import time
import academicIO
from enums import Bank, EncoderChannel, EncoderMode

# specify the bank and the encoder channel
bank = Bank.A
channel = EncoderChannel.ENC0
# specify the mode of operation for communicating with the encoder device
mode = EncoderMode.QUADRATURE

# open an encoder session, and set initial values for the parameters
with academicIO.Encoder(bank, channel, mode) as encoder:
    # specify whether to reset the encoder device. To reset the encoder, set
    # reset_counter to True
    reset_counter = True
    # reset the counter value and counter direction of the the encoder device
    encoder.read(reset_counter)

    # specify not to reset the encoder in order to keep the counter value and
    # the counter direction since last counter reset
    reset_counter = False
    # The program generates and reads values 20 times
    for x in range(0, 20):
        # read the counter value and direction of the counter from the encoder
        # since last counter read
        counter_value, counter_direction_decrease = encoder.read(reset_counter)
        # print the counter value. The counter value must be in the range
        # -2,147,483,648 to 2,147,483,647
        print counter_value,
        # print the counter direction
        if counter_direction_decrease:
            print ", direction is decreasing"
        else:
            print ", direction is increasing"

        # delay for 1.5 seconds so that the program does not run too fast
        time.sleep(1.5)