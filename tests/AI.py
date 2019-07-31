"""
Hardware setup:
  1. Connect AI2 and +3.3V on connector A.
  2. Connect AI6 and +5V on connector A.
"""
import unittest
import time
import pytest
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A

class TestReadSingleChannel(unittest.TestCase):
    def setUp(self):
        self.AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})

    def tearDown(self):
        self.AI_single_channel.close()

    def test_singlePoint(self):
        value_array = self.AI_single_channel.read()
        for value in value_array:
            assert value == pytest.approx(3.3, 0.1)

class TestReadMultipleChannels(unittest.TestCase):
    def setUp(self):
        self.AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                                           {'bank': bank, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

    def tearDown(self):
        self.AI_multiple_channels.close()

    def test_singlePoint(self):
        value_array = self.AI_multiple_channels.read()
        for index, value in enumerate(value_array):
            if index == 0:
                assert value == pytest.approx(3.3, 0.1)
            else:
                assert value == pytest.approx(-1.7, 0.1)

class TestOpenAssertion(unittest.TestCase):
    def test_invalidBank(self):
        assertion = False
        try:
            academicIO.AnalogInput({'bank': 'C', 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})
        except (AssertionError) as err:
            assertion = True
        self.assertTrue(assertion, 'Caught the error fail - The banks available in the AI normal mode are A and B.')

    def test_invalidChannelInSingleEndedMode(self):
        assertion = False
        try:
            academicIO.AnalogInput({'bank': bank, 'channel': 8, 'mode': AIMode.SINGLE_ENDED})
        except (AssertionError) as err:
            assertion = True
        self.assertTrue(assertion, 'Caught the error fail - The channels available in the AI single ended mode are AI0 - 7.')

    def test_invalidChannelInDifferentialMode(self):
        assertion = False
        try:
            academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI4, 'mode': AIMode.DIFFERENTIAL})
        except (AssertionError) as err:
            assertion = True
        self.assertTrue(assertion, 'Caught the error fail - The channels available in the AI differential mode are AI0 - 3.')

    def test_invalidRange(self):
        assertion = False
        try:
            academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': '+/-20V'})
        except (AssertionError) as err:
            assertion = True
        self.assertTrue(assertion, 'Caught the error fail - The range value of the channel should be in AIRange.')
