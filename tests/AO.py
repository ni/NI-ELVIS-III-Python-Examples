"""
Hardware setup:
    1. Connect AI0 and AO0 on connector A.
    2. Connect AI3 and AO1 on connector A.
    3. Connect AI0 and AO0 on connector B.
    3. Connect AI3 and AO1 on connector B.
"""
import unittest
import time
import pytest
import threading

from nielvis import AnalogOutput, AnalogInput, Bank, AOChannel, AIChannel

bank = Bank.A
limits = { 'sampleRate': { 'min': 1, 'max': 1600000}}

class Test_AnalogOutput_WriteSingleChannel(unittest.TestCase):
    def setUp(self):
        self.AO_single_channel = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
        self.AI_single_channel = AnalogInput({'bank': bank, 'channel': AIChannel.AI0})

    def tearDown(self):
        self.AO_single_channel.close()
        self.AI_single_channel.close()

    def test_OpeWriteMultiplePointsCloseRepeatedly_DoesnotShowAnyError(self):
        sample_rate = 1000
        input_value = [1.1, 2.2]
        AO0_in_bank_A = AnalogOutput({'bank': Bank.A, 'channel': AOChannel.AO0})
        AO0_in_bank_B = AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0})

        AO0_in_bank_A.write(input_value, sample_rate)
        AO0_in_bank_B.write(input_value, sample_rate)

        AO0_in_bank_B.close()

        AO0_in_bank_A.write(input_value, sample_rate)
        AO0_in_bank_A.close()

    def test_WriteLargeNumberOfValuesWithTenThousandSampleRate_DoesnotShowAnyError(self):
        sample_rate = 10000
        input_value = [3.3 for i in range(55555)]
        
        self.AO_single_channel.write(input_value, sample_rate)


class Test_AnalogOutput_OpenAssertion(unittest.TestCase):
    def test_OpenWithInvalidBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogOutput({'bank': 'C', 'channel': AOChannel.AO0})

    def test_OpenWithInvalidChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogOutput({'bank': bank, 'channel': 2})

    def test_OpenWithoutBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogOutput({'channel': AOChannel.AO0})

    def test_OpenWithoutChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogOutput({'bank': bank})


class Test_AnalogOutput_WriteAssertion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.AO = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})

    @classmethod
    def tearDownClass(self):
        self.AO.close()

    def test_WriteWithInvalidNumberOfArguments_ShowAssertion(self):        
        with self.assertRaises(TypeError):
            self.AO.write()

        with self.assertRaises(TypeError):
            self.AO.write(1000, 1000, 1000)
    
    def test_WriteOneSampleWithInvalidValue_ShowAssertion(self):
        testcases = [
            'a',
            '',
            [],
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                self.AO.write(testcase)

    def test_WriteNSampleWithInvalidValues_ShowAssertion(self):       
        sample_rate = 1000
        testcases = [
            [3.5, 'a'],
            [3.5, []],
            '',
            5,
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                self.AO.write(testcase, sample_rate)

    def test_WriteNSampleWithInvalidSampleRate_ShowAssertion(self):        
        values = [3.5]
        testcases = [
            '',
            [],
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                self.AO.write(values, testcase)
    
    def test_PassSampleRateThatIsGreaterThanMax_ShowAssertion(self):
        values = [3.5]

        with self.assertRaises(AssertionError):
            self.AO.write(values, limits['sampleRate']['max'] + 1)

    def test_PassSampleRateThatIsLessThanMin_ShowAssertion(self):
        values = [3.5]

        with self.assertRaises(AssertionError):
            self.AO.write(values, limits['sampleRate']['min'] - 1)


class Test_AnalogInput_StartAssertion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.expectedInput = [[0,1]]
        self.expectedSampleRate = 1000
        self.expectedTimeout = -1

    def setUp(self):
        self.AO_single_channel = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
        self.AO_multiple_channels = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                 {'bank': bank, 'channel': AOChannel.AO1})

    def tearDown(self):
        self.AO_single_channel.close()
        self.AO_multiple_channels.close()

    def test_PassInvalidInputValues_ShowAssertion(self):
        wrong_values = [0, [], [[]]]

        for wrong_value in wrong_values:
            with self.assertRaises(AssertionError):
                self.AO_single_channel.start_continuous_mode(wrong_value, self.expectedSampleRate, self.expectedTimeout)
            
    def test_PassInvalidNumberOfInputValues_ShowAssertion(self):
        wrong_values = [[1], [[1]], [[1], ['a']]]

        for wrong_value in wrong_values:
            with self.assertRaises(AssertionError):
                self.AO_multiple_channels.start_continuous_mode(wrong_value, self.expectedSampleRate, self.expectedTimeout)
                
    def test_PassInvalidSampleRateToSingleChannel_ShowAssertion(self):
        limits = {'SampleRate': {'min': 1000, 'max': 1600000}}
        wrong_sample_rates = [limits['SampleRate']['min'] - 1, limits['SampleRate']['max'] + 1]

        for wrong_sample_rate in wrong_sample_rates:
            with self.assertRaises(AssertionError):
                self.AO_single_channel.start_continuous_mode(self.expectedInput, wrong_sample_rate, self.expectedTimeout)
