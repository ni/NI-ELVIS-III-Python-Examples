"""
NI ELVIS III Encoder Example
This example illustrates how to read and decode signals from an encoder
through the encoder channels on NI ELVIS III. To create an Encoder session,
you need to define two parameters: bank and channel. To read and decode to the
encoder device, you need to define one parameter: reset_counter. This is an
optional parameter. The default values of the optional parameter is:
    reset_counte: False

Hardware setup:
	1. Connect connector A phase A (default is DIO0) to ENC.A of a device.
	2. Connect connector A phase B (default is DIO1) to ENC.B of a device.

Output:
	The program reads the counter value and the counter direction from the device.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, EncoderChannel, EncoderMode

# specify bank and channel to read and decode signals from the encoder
bank = Bank.A
channel = EncoderChannel.ENC0
# Encoder: specify the mode of operation for communicating with the UART
# device
mode = EncoderMode.QUADRATURE

# open an Encoder session, and set initial values for the parameters
with NIELVISIIIAcademicIO.Encoder(bank, channel, mode) as encoder:
    # specify whether to reset the encoder tick counter to zero, True = reset
    reset_counter = True
    # reset the counter
    encoder.read(reset_counter)

    # specify whether to reset the encoder tick counter to zero, False = not reset
    reset_counter = False
    # The program reads values 20 times
    for x in range(0, 20):
        # read the number of ticks and direction of the counter that this
        # example read from the encoder since last counter reset
        counter_value, counter_direction_decrease = encoder.read(reset_counter)
        # print the counter value
        # the counter value must be in the range [-2,147,483,648:2,147,483,647]
        print counter_value,
        # print the counter direction
        if counter_direction_decrease:
            print ", direction is decreasing"
        else:
            print ", direction is increasing"

        # delay for 1.5 seconds so that the program does not run too fast
        time.sleep(1.5)