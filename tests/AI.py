"""
Hardware setup:
  1. Connect AI2 and +3.3V on connector A.
  2. Connect AI6 and +5V on connector A.
"""
import time
import pytest
import academicIO
from enums import *

bank = Bank.A
AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})
AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                                        {'bank': bank, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

value_array = AI_single_channel.read()
for value in value_array:
    print value,
    assert value == pytest.approx(3.3, 0.1)
print 

value_array = AI_multiple_channels.read()
for index, value in enumerate(value_array):
    print value,
    if index == 0:
        assert value == pytest.approx(3.3, 0.1)
    else:
        assert value == pytest.approx(-1.7, 0.1)
print

AI_single_channel.close()
AI_multiple_channels.close()

try:
    academicIO.AnalogInput({'bank': 'C', 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})
except (AssertionError) as err:
    print "Caught the error - The banks available in the AI normal mode are A and B."

try:
    academicIO.AnalogInput({'bank': bank, 'channel': 8, 'mode': AIMode.SINGLE_ENDED})
except (AssertionError) as err:
    print "Caught the error - The channels available in the AI normal mode are AI0 - 7."

try:
    academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI4, 'mode': AIMode.DIFFERENTIAL})
except (AssertionError) as err:
    print "Caught the error - The channels available in the AI differential mode are AI0 - 3."

try:
    academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': '+/-20V'})
except (AssertionError) as err:
    print "Caught the error - The range value of the channel should be in AIRange."