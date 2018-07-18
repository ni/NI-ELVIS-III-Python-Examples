"""
NI ELVIS III Encoder Example
This example illustrates how to read and decode signals from an encoder
through the encoder channels on the NI ELVIS III. The program first defines
the configuration for the ender channels, then reads the encoder channels in a
loop. Each time the read is called a list of data is returned for the channels.
The list of data contains counter value and counter direction. The time
between reads is not precisely timed, and is controlled by a software delay.

The encoder configuration consists of three parameters: bank, channel, and
mode. There are two identical banks of encoder port (A and B). Each
encoder channel contains two phases which represents to two DIO channels as
indicated in this table:
    ENC0: phase A (DIO0) and phase B (DIO1)
    ENC1: phase A (DIO2) and phase B (DIO3)
    ENC2: phase A (DIO4) and phase B (DIO5)
    ENC3: phase A (DIO6) and phase B (DIO7)
    ENC4: phase A (DIO8) and phase B (DIO9)
    ENC5: phase A (DIO10) and phase B (DIO11)
    ENC6: phase A (DIO12) and phase B (DIO13)
    ENC7: phase A (DIO14) and phase B (DIO15)
    ENC8: phase A (DIO16) and phase B (DIO17)
    ENC9: phase A (DIO18) and phase B (DIO19)
The encoder communication can be configured to quadrature mode or step and
direction mode.

This example illustrates how to use 2pcs KY-040 Arduino Rotary under the
quadrature mode. See
http://henrysbench.capnfatz.com/henrys-bench/arduino-sensors-and-input/keyes-ky-040-arduino-rotary-encoder-user-manual/
for more details.

This example uses:
    1. Bank A, Channel DIO0.
    2. Bank A, Channel DIO1.

Hardware setup:
    1. Connect ENC0 phase A (DIO0) on bank A to ENC.A of a encoder
       device.
    2. Connect ENC0 phase B (DIO1) on bank A to ENC.B of a encoder
       device.

Result:
    Twenty data (counter value and the counter direction) acquired from the
    encoder device. The data changes when the knob on the KY-040 Arduino
    Rotary is rotated.
"""
import time
import academicIO
from enums import Bank, EncoderChannel, EncoderMode

# specify the bank and the encoder channel
bank = Bank.A
channel = EncoderChannel.ENC0
# specify the mode of operation for communicating with the encoder device
mode = EncoderMode.QUADRATURE

# open an encoder session
with academicIO.Encoder(bank, channel, mode) as encoder:
    # specify whether to reset the encoder device. To reset the encoder, set
    # reset_counter to True
    reset_counter = True
    # reset the counter value and counter direction of the the encoder device
    encoder.read(reset_counter)

    # specify not to reset the encoder in order to keep the counter value and
    # the counter direction since last counter reset
    reset_counter = False
    # generates and reads values 20 times
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

        # add a short delay before acquiring next data point
        time.sleep(1.5)
