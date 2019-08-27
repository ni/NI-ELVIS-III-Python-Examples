"""
Hardware setup:
	1. Connect connector A phase A (DIO18) to ENC.A of ADXL345.
	2. Connect connector A phase B (DIO19) to ENC.B of ADXL345.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
channel = EncoderChannel.ENC9
with academicIO.Encoder(bank, channel, EncoderMode.QUADRATURE) as encoder_quadrature_mode:
    reset_counter = True
    encoder_quadrature_mode.read(reset_counter)
    reset_counter = False
    for x in range(0, 5):
        counter_value, counter_direction_decrease = encoder_quadrature_mode.read(reset_counter)
        print(counter_value)
        if counter_direction_decrease:
        	print(", direction is decreasing")
        else:
        	print(", direction is increasing")

        time.sleep(1)

print("done")

with academicIO.Encoder(bank, channel, EncoderMode.STEP_AND_DIRECTION) as encoder_step_mode:
    reset_counter = True
    encoder_step_mode.read(reset_counter)
    reset_counter = False
    for x in range(0, 5):
        counter_value, counter_direction_decrease = encoder_step_mode.read(reset_counter)
        print(counter_value)
        if counter_direction_decrease:
        	print(", direction is decreasing")
        else:
        	print(", direction is increasing")

        time.sleep(1)