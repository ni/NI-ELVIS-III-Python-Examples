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
            self.assertEqual(value, pytest.approx(3.3, 0.1))

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
                self.assertEqual(value, pytest.approx(3.3, 0.1))
            else:
                self.assertEqual(value, pytest.approx(-1.7, 0.1))

class TestOpenAssertion(unittest.TestCase):
    def test_invalidBank(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogInput({'bank': 'C', 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})

    def test_invalidChannelInSingleEndedMode(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogInput({'bank': bank, 'channel': 8, 'mode': AIMode.SINGLE_ENDED})

    def test_invalidChannelInDifferentialMode(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI4, 'mode': AIMode.DIFFERENTIAL})

    def test_invalidRange(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI2, 'range': '+/-20V'})
