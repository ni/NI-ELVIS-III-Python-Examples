"""
Hardware setup:
  1. Connect AI2 and +3.3V on connector A.
  2. Connect AI6 and +5V on connector A.
"""
import time
import pytest
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})
AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                              {'bank': bank, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

value_array = AI_single_channel.read()
for value in value_array:
    print(value)
    assert value == pytest.approx(3.3, 0.1), "The value read from single channel should be approx to 3.3"

value_array = AI_multiple_channels.read()
for index, value in enumerate(value_array):
    print(value)
    if index == 0:
        assert value == pytest.approx(3.3, 0.1), "The value read from multiple channels should be approx to 3.3"
    else:
        assert value == pytest.approx(-1.7, 0.1), "The value read from multiple channels should be approx to -1.7"

number_of_samples = 10
sample_rate = 1000
value_array = AI_multiple_channels.read(number_of_samples, sample_rate)
value_array_for_first_channel = value_array[0][0]
value_array_for_second_channel = value_array[0][1]
assert len(value_array_for_first_channel) == number_of_samples, "The number of read back values is not equal to %s" % (number_of_samples) 
assert len(value_array_for_second_channel) == number_of_samples, "The number of read back values is not equal to %s" % (number_of_samples) 
assert all(float(value) == pytest.approx(3.3, 0.1) for value in value_array_for_first_channel)  == True, "The value read from multiple channels should be approx to 3.3"
assert all(float(value) == pytest.approx(-1.7, 0.1) for value in value_array_for_second_channel) == True, "The value read from multiple channels should be approx to -1.7"

AI_single_channel.close()
AI_multiple_channels.close()

try:
    academicIO.AnalogInput({'bank': 'C', 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})
except (AssertionError) as err:
    print("Caught the error - The banks available in the AI normal mode are A and B.")

try:
    academicIO.AnalogInput({'bank': bank, 'channel': 8, 'mode': AIMode.SINGLE_ENDED})
except (AssertionError) as err:
    print("Caught the error - The channels available in the AI normal mode are AI0 - 7.")

try:
    academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI4, 'mode': AIMode.DIFFERENTIAL})
except (AssertionError) as err:
    print("Caught the error - The channels available in the AI differential mode are AI0 - 3.")

try:
    academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': '+/-20V'})
except (AssertionError) as err:
    print("Caught the error - The range value of the channel should be in AIRange.")

AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})
approx_number_of_samples = 10
approx_samples_rate = 1000
try:
    AI_single_channel.read(10)
except (TypeError) as err:
    print("Caught the error - The paramerters do not meet the conditions. (1 parameter)")
try:
    AI_single_channel.read(10, 10, 10)
except (TypeError) as err:
    print("Caught the error - The paramerters do not meet the conditions. (3 parameters)")
try:
    AI_single_channel.read(-1, approx_samples_rate)
except (AssertionError) as err:
    print("Caught the error - Number of samples should be greater or equal than 0")
try:
    AI_single_channel.read(10001, approx_samples_rate)
except (AssertionError) as err:
    print("Caught the error - Number of samples should be less or equal than 10000")
try:
    AI_single_channel.read(approx_number_of_samples, 0)
except (AssertionError) as err:
    print("Caught the error - Number of samples should be greate or equal than 1")
try:
    AI_single_channel.read(approx_number_of_samples, 1000001)
except (AssertionError) as err:
    print("Caught the error - Number of samples should be less or equal than 1000000")
AI_single_channel.close()
