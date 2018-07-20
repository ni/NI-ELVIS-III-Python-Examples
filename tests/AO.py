"""
Hardware setup:
    1. Connect AI0 and AO0 on connector A.
    2. Connect AI3 and AO1 on connector A.
"""
import time
import pytest
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
AO_single_channel = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
AO_multiple_channels = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                         {'bank': bank, 'channel': AOChannel.AO1})
AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                                                        {'bank': bank, 'channel': AIChannel.AI3})

input_value = 3.5
AO_multiple_channels.write(input_value)
value_array = AI_multiple_channels.read()
for value in value_array:
    print value,
    assert value == pytest.approx(input_value, 0.1)
print 

input_new_value = 2.0       
AO_single_channel.write(input_new_value)
value_array = AI_multiple_channels.read()
for index, value in enumerate(value_array):
    print value,
    if index == 0:
        assert value == pytest.approx(input_new_value, 0.1)
    else:
        assert value == pytest.approx(input_value, 0.1)
print

input_value = 0.5
AO_multiple_channels.write(input_value)
value_array = AI_multiple_channels.read()
for value in value_array:
    print value,
    assert value == pytest.approx(input_value, 0.1)
print

AO_single_channel.close()
AO_multiple_channels.close()
AI_multiple_channels.close()

try:
    academicIO.AnalogOutput({'bank': bank, 'channel': 2})
except (AssertionError) as err:
    print "Caught the error - The channels available in the AO should be 0-1."