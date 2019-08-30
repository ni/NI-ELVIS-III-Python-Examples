"""
Hardware setup:
	1. Connect connector A phase A (DIO18) to ENC.A (CLK) of the key.
	2. Connect connector A phase B (DIO19) to ENC.B (DL) of the key.
"""
import time
import unittest
from nielvis import Encoder, EncoderChannel, EncoderMode, Bank

bank = Bank.A
channel = EncoderChannel.ENC9

class Test_Encoder(unittest.TestCase):
    def __print(self, counter_value, counter_direction_decrease):
        print(counter_value, end = '')
        if counter_direction_decrease:
            print(", direction is decreasing")
        else:
            print(", direction is increasing")

    def test_ReadWithQuadratureMode_DoesnotShowError(self):
        with Encoder(bank, channel, EncoderMode.QUADRATURE) as encoder_quadrature_mode:
            reset_counter = True
            encoder_quadrature_mode.read(reset_counter)
            reset_counter = False
            for x in range(0, 5):
                counter_value, counter_direction_decrease = encoder_quadrature_mode.read(reset_counter)
                self.__print(counter_value, counter_direction_decrease)
                time.sleep(1)
    
    def test_ReadWithStepAndDirectionMode_DoesnotShowError(self):
        with Encoder(bank, channel, EncoderMode.STEP_AND_DIRECTION) as encoder_step_mode:
            reset_counter = True
            encoder_step_mode.read(reset_counter)
            reset_counter = False
            for x in range(0, 5):
                counter_value, counter_direction_decrease = encoder_step_mode.read(reset_counter)
                self.__print(counter_value, counter_direction_decrease)
                time.sleep(1)
