"""
Hardware setup:
    1. Connect AI0 and AO0 on connector A.
    2. Connect AI3 and AO1 on connector A.
"""
import unittest
import time
import pytest
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A

class Test_AnalogOutput_WriteSingleChannel(unittest.TestCase):
    def setUp(self):
        self.AO_single_channel = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
        self.AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0})

    def tearDown(self):
        self.AO_single_channel.close()
        self.AI_single_channel.close()

    def test_WriteSinglePoint_ReturnExpectedReadBack(self):
        input_value = 2.0       
        self.AO_single_channel.write(input_value)
        value_array = self.AI_single_channel.read()
        for value in value_array:
            self.assertEqual(value, pytest.approx(input_value, 0.1))

    def test_WriteSinglePoint_ReturnDifferentValueFromEachChannel(self):
        AO_multiple_channels = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                       {'bank': bank, 'channel': AOChannel.AO1})
        AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                                                      {'bank': bank, 'channel': AIChannel.AI3})
        input_value_for_single_channels = 2.5
        input_value_for_multiple_channels = 3.3
        AO_multiple_channels.write(input_value_for_multiple_channels)
        self.AO_single_channel.write(input_value_for_single_channels)
        value_array = AI_multiple_channels.read()
        for index, value in enumerate(value_array):
            if index == 0:
                self.assertEqual(value, pytest.approx(input_value_for_single_channels, 0.1))
            else:
                self.assertEqual(value, pytest.approx(input_value_for_multiple_channels, 0.1))

        AO_multiple_channels.close()
        AI_multiple_channels.close()

class Test_AnalogOutput_WriteTwoChannels(unittest.TestCase):
    def setUp(self):
        self.AO_multiple_channels = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                            {'bank': bank, 'channel': AOChannel.AO1})
        self.AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                                                           {'bank': bank, 'channel': AIChannel.AI3})
    
    def tearDown(self):
        self.AO_multiple_channels.close()
        self.AI_multiple_channels.close()

    def test_WriteSinglePoint_ReturnExpectedReadBack(self):
        input_value = 3.5
        self.AO_multiple_channels.write(input_value)
        value_array = self.AI_multiple_channels.read()
        for value in value_array:
            self.assertEqual(value, pytest.approx(input_value, 0.1))

class Test_AnalogOutput_Assertion(unittest.TestCase):
    def test_OpenWithInvalidBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogOutput({'bank': bank, 'channel': 2})
