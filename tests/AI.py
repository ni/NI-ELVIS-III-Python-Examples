"""
Hardware setup:
  1. Connect AI2 and +3.3V on connector A.
  2. Connect AI6 and +5V on connector A.
  2. Connect AI7 and +3.3V on connector B.
"""
import unittest
import time
import pytest

from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

bankA = Bank.A
bankB = Bank.B
limits = { 'numberOfSamples': { 'min': 0, 'max': 10000 }, 'sampleRate': { 'min': 1, 'max': 1000000 }}

class Test_AnalogInput_ReadSingleChannelFromBankA(unittest.TestCase):
    def setUp(self):
        self.AI_single_channel = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})

    def tearDown(self):
        self.AI_single_channel.close()

    def checkMultiplePointsReadBackValues(self, value_array, number_of_samples):
        value_array_for_first_channel = value_array[0][0]
        self.assertEqual(len(value_array_for_first_channel), number_of_samples)
        for value in value_array_for_first_channel:
            self.assertEqual(float(value), pytest.approx(3.3, 0.1))

    def test_ReadSinglePointOnce_ReturnExpectedReadBack(self):
        value_array = self.AI_single_channel.read()
        for value in value_array:
            self.assertEqual(value, pytest.approx(3.3, 0.1))

    def test_ReadSinglePointTwentyTimes_ReturnExpectedReadBack(self):
        for i in range(0, 20):
            value_array = self.AI_single_channel.read()
            for value in value_array:
                self.assertEqual(value, pytest.approx(3.3, 0.1))

    def test_ReadZeroPointWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['min']
        sample_rate = 1000
        
        value_array = self.AI_single_channel.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenThousandPointsWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['max']
        sample_rate = 1000
        
        value_array = self.AI_single_channel.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenPointsWithOneSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10
        sample_rate = limits['sampleRate']['min']
        
        value_array = self.AI_single_channel.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenPointsWithOneMillionSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10
        sample_rate = limits['sampleRate']['max']
        
        value_array = self.AI_single_channel.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ContinuousMode_ReadOnePointWithOneSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['min']
        sample_rate = limits['sampleRate']['min']
        timeout = -1
        
        self.AI_single_channel.start_continuous_mode(sample_rate)
        value_array = self.AI_single_channel.read(number_of_samples, timeout)
        self.AI_single_channel.stop_continuous_mode()

        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ContinuousMode_ReadTenKPointsWithOneMillionSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10000
        sample_rate = limits['sampleRate']['max']
        timeout = -1
        
        self.AI_single_channel.start_continuous_mode(sample_rate)
        value_array = self.AI_single_channel.read(number_of_samples, timeout)
        self.AI_single_channel.stop_continuous_mode()

        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ContinuousMode_ReadTenKPointsWithFiveKSampleRateAndTwnetyOneKTimeout_ReturnExpectedReadBack(self):
        number_of_samples = 10000
        sample_rate = 5000
        timeout = 2100
        
        self.AI_single_channel.start_continuous_mode(sample_rate)
        value_array = self.AI_single_channel.read(number_of_samples, timeout)
        self.AI_single_channel.stop_continuous_mode()

        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ContinuousMode_ReadOnePointWithOneSampleRateAndCloseWithoutStop_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['min']
        sample_rate = limits['sampleRate']['min']
        timeout = -1
        
        self.AI_single_channel.start_continuous_mode(sample_rate)
        value_array = self.AI_single_channel.read(number_of_samples, timeout)

        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

class Test_AnalogInput_ReadSingleChannelFromBankB(unittest.TestCase):
    def setUp(self):
        self.AI_single_channel = AnalogInput({'bank': bankB, 'channel': AIChannel.AI7, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})

    def tearDown(self):
        self.AI_single_channel.close()

    def checkMultiplePointsReadBackValues(self, value_array, number_of_samples):
        value_array_for_first_channel = value_array[0][0]
        self.assertEqual(len(value_array_for_first_channel), number_of_samples)
        for value in value_array_for_first_channel:
            self.assertEqual(float(value), pytest.approx(3.3, 0.1))

    def test_ContinuousMode_Read2222PointsWith500SampleRateAnd2000Timeout_ReturnExpectedReadBack(self):
        number_of_samples = 2222
        sample_rate = 1200
        timeout = -1
        
        self.AI_single_channel.start_continuous_mode(sample_rate)
        value_array = self.AI_single_channel.read(number_of_samples, timeout)
        self.AI_single_channel.stop_continuous_mode()

        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

class Test_AnalogInput_ReadTwoChannelsFromBankA(unittest.TestCase):
    def setUp(self):
        self.AI_multiple_channels = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                                {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

    def tearDown(self):
        self.AI_multiple_channels.close()

    def checkMultiplePointsReadBackValues(self, value_array, number_of_samples):
        number_of_samples_for_multi_channels = number_of_samples
        value_array_for_first_channel = value_array[0][0]
        value_array_for_second_channel = value_array[0][1]
        self.assertEqual(len(value_array_for_first_channel), number_of_samples_for_multi_channels)
        self.assertEqual(len(value_array_for_second_channel), number_of_samples_for_multi_channels)
        for value in value_array_for_first_channel:
            self.assertEqual(float(value), pytest.approx(3.3, 0.1))
        for value in value_array_for_second_channel:
            self.assertEqual(float(value), pytest.approx(-1.7, 0.1))

    def test_ReadSinglePointOnce_ReturnExpectedReadBack(self):
        value_array = self.AI_multiple_channels.read()
        for index, value in enumerate(value_array):
            if index == 0:
                self.assertEqual(value, pytest.approx(3.3, 0.1))
            else:
                self.assertEqual(value, pytest.approx(-1.7, 0.1))

    def test_ReadSinglePointTwentyTimes_ReturnExpectedReadBack(self):
        for i in range(0, 20):
            value_array = self.AI_multiple_channels.read()
            for index, value in enumerate(value_array):
                if index == 0:
                    self.assertEqual(value, pytest.approx(3.3, 0.1))
                else:
                    self.assertEqual(value, pytest.approx(-1.7, 0.1))

    def test_ReadZeroPointWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['min']
        sample_rate = 1000
        
        value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenThousandPointsWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = limits['numberOfSamples']['max']
        sample_rate = 1000
        
        value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenPointsWithOneSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10
        sample_rate = limits['sampleRate']['min']
        
        value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ReadTenPointsWithFiveKSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10
        sample_rate = limits['sampleRate']['max'] / 2
        
        value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

    def test_ContinuousMode_ReadTenPointsWith250KSampleRate_ReturnExpectedReadBack(self):
        number_of_samples = 10
        sample_rate = 250000
        timeout = -1
        
        self.AI_multiple_channels.start_continuous_mode(sample_rate)
        value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)
        self.AI_multiple_channels.stop_continuous_mode()
        
        self.checkMultiplePointsReadBackValues(value_array, number_of_samples)

class Test_AnalogInput_OpenTwoNsampleAtTheSameTime(unittest.TestCase):
    def open_first_ai(self):
        self.first_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                    {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})
    def open_second_ai(self):
        self.second_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI6, 'range': AIRange.PLUS_OR_MINUS_10V})

    def close_first_ai(self):
        self.first_ai.close()

    def close_second_ai(self):
        self.second_ai.close()

    def checkReadbankValue(self, value_array, expected_value, expected_number_of_samples):
        self.assertEqual(len(value_array), expected_number_of_samples)
        for value in value_array:
            self.assertEqual(float(value), pytest.approx(expected_value, 0.1))

    def test_ReadTwoAiNsampleAndCloseItThenReadAgain_ReturnExpectedReadBack(self):
        number_of_samples = 100
        sample_rate = 1000
        self.open_first_ai()
        self.open_second_ai()
        
        first_ai_value_array = self.first_ai.read(number_of_samples, sample_rate)
        second_ai_value_array = self.second_ai.read(number_of_samples, sample_rate)

        self.checkReadbankValue(first_ai_value_array[0][0], 3.3, number_of_samples)
        self.checkReadbankValue(first_ai_value_array[0][1], -1.7, number_of_samples)
        self.checkReadbankValue(second_ai_value_array[0][0], 5, number_of_samples)

        self.close_first_ai()
        self.close_second_ai()

        self.open_first_ai()

        first_ai_value_array = self.first_ai.read(number_of_samples, sample_rate)

        self.checkReadbankValue(first_ai_value_array[0][0], 3.3, number_of_samples)
        self.checkReadbankValue(first_ai_value_array[0][1], -1.7, number_of_samples)

        self.close_first_ai()

class Test_AnalogInput_OpenTwoContinuousAtTheSameTime(unittest.TestCase):
    def checkReadbankValue(self, value_array, expected_value, expected_number_of_samples):
        self.assertEqual(len(value_array), expected_number_of_samples)
        for value in value_array:
            self.assertEqual(float(value), pytest.approx(expected_value, 0.1))

    def test_ContinuousMode_ReadTwoChannelsAndCloseItThenReadAgain_ReturnExpectedReadBack(self):
        sample_rate = 1000
        number_of_samples = 2
        timeout = -1

        first_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})
        second_ai = AnalogInput({'bank': bankB, 'channel': AIChannel.AI7, 'range': AIRange.PLUS_OR_MINUS_10V})
        
        first_ai.start_continuous_mode(sample_rate)
        second_ai.start_continuous_mode(sample_rate)

        first_ai_value_array = first_ai.read(number_of_samples, timeout)
        second_ai_value_array = first_ai.read(number_of_samples, timeout)

        self.checkReadbankValue(first_ai_value_array[0][0], 3.3, number_of_samples)
        self.checkReadbankValue(first_ai_value_array[0][1], -1.7, number_of_samples)
        self.checkReadbankValue(second_ai_value_array[0][0], 3.3, number_of_samples)

        first_ai.stop_continuous_mode()
        second_ai.stop_continuous_mode()

        first_ai.close()
        second_ai.close()

        first_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                    {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

        first_ai.start_continuous_mode(sample_rate)

        first_ai_value_array = first_ai.read(number_of_samples, timeout)

        self.checkReadbankValue(first_ai_value_array[0][0], 3.3, number_of_samples)
        self.checkReadbankValue(first_ai_value_array[0][1], -1.7, number_of_samples)

        first_ai.stop_continuous_mode()

        first_ai.close()

    def test_ContinuousMode_StartTwoAiInSameBank_ShowAssertion(self):
        sample_rate = 1000
        first_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V})
        second_ai = AnalogInput({'bank': bankA, 'channel': AIChannel.AI7, 'range': AIRange.PLUS_OR_MINUS_10V})
        
        first_ai.start_continuous_mode(sample_rate)
        with self.assertRaises(AssertionError):
            second_ai.start_continuous_mode(sample_rate)

        first_ai.stop_continuous_mode()
        first_ai.close()
        second_ai.close()

class Test_AnalogInput_OpenAssertion(unittest.TestCase):
    def test_OpenWithoutBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})

    def test_OpenWithoutChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'bank': bankA, 'mode': AIMode.SINGLE_ENDED})

    def test_OpenWithoutMode_DoesnotShowAssertion(self):
            AnalogInput({'bank': bankA, 'channel': AIChannel.AI0, 'range': AIRange.PLUS_OR_MINUS_10V})

    def test_OpenWithoutRange_DoesnotShowAssertion(self):
            AnalogInput({'bank': bankA, 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})

    def test_OpenWithInvalidBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'bank': 'C', 'channel': AIChannel.AI0, 'mode': AIMode.SINGLE_ENDED})

    def test_OpenWithInvalidChannelInSingleEndedMode_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'bank': bankA, 'channel': 8, 'mode': AIMode.SINGLE_ENDED})

    def test_OpenWithInvalidChannelInDifferentialMode_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'bank': bankA, 'channel': AIChannel.AI4, 'mode': AIMode.DIFFERENTIAL})

    def test_OpenWithInvalidRange_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': '+/-20V'})   

class Test_AnalogInput_ReadAssertion(unittest.TestCase):
    def setUp(self):
        self.AI_single_channel = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})
        self.AI_multiple_channels = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                                {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

    @classmethod
    def setUpClass(self):
        self.approx_number_of_samples = 10
        self.approx_samples_rate = 1000

    def tearDown(self):
        self.AI_single_channel.close()
        self.AI_multiple_channels.close()

    def test_PassOneArgumentToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(TypeError):
            self.AI_single_channel.read(10)

    def test_PassThreeArgumentsToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(TypeError):
            self.AI_single_channel.read(10, 10, 10)
        
    def test_PassNumberOfSamplesThatGreaterThanMaxToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.read(limits['numberOfSamples']['max'] + 1, self.approx_samples_rate)

    def test_PassNumberOfSamplesThatLessThanMinToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.read(limits['numberOfSamples']['min'] - 1, self.approx_samples_rate)

    def test_PassMaxSampleRateToReadTwoChannels_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_multiple_channels.read(self.approx_number_of_samples, limits['sampleRate']['max'])

    def test_PassSampleRateThatGreaterThanMaxToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.read(self.approx_number_of_samples, limits['sampleRate']['max'] + 1)

    def test_PassSampleRateThatLessThanMinToReadOneChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.read(self.approx_number_of_samples, limits['sampleRate']['min'] - 1)

class Test_AnalogInput_StartAssertion(unittest.TestCase):
    def setUp(self):
        self.AI_single_channel = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_5V, 'mode': AIMode.SINGLE_ENDED})
        self.AI_multiple_channels = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2, 'range': AIRange.PLUS_OR_MINUS_10V},
                                                {'bank': bankA, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL})

    @classmethod
    def setUpClass(self):
        self.sample_rate_limits_for_multiple_channels = {'max': 250000, 'min': 1}

    def tearDown(self):
        self.AI_single_channel.close()
        self.AI_multiple_channels.close()

    def test_PassSampleRateThatLessThanMinToSingleChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.start_continuous_mode(limits['sampleRate']['min'] - 1)

    def test_PassSampleRateThatGreaterThanMaxToSingleChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_single_channel.start_continuous_mode(limits['sampleRate']['max'] + 1)

    def test_PassSampleRateThatLessThanMinToTwoChannels_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_multiple_channels.start_continuous_mode(self.sample_rate_limits_for_multiple_channels['min'] - 1)

    def test_PassSampleRateThatGreaterThanMaxToTwoChannels_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.AI_multiple_channels.start_continuous_mode(self.sample_rate_limits_for_multiple_channels['max'] + 1)

class Test_AnalogInput_CalculateSampleRateToTicks(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.AI = AnalogInput({'bank': bankA, 'channel': AIChannel.AI2})

    @classmethod
    def tearDownClass(self):
        self.AI.close()

    def test_GivenMin_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(limits['sampleRate']['min'])

        self.assertEqual(count, 40000)
        self.assertEqual(actual_sample_rate, 1000)

    def test_GivenAThousand_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(1000)

        self.assertEqual(count, 40000)
        self.assertEqual(actual_sample_rate, 1000)

    def test_GivenFiveThousand_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(5000)

        self.assertEqual(count, 8000)
        self.assertEqual(actual_sample_rate, 5000)

    def test_GivenTenThousand_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(10000)

        self.assertEqual(count, 4000)
        self.assertEqual(actual_sample_rate, 10000)

    def test_GivenFiftyThousand_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(50000)

        self.assertEqual(count, 1333)
        self.assertEqual(actual_sample_rate, pytest.approx(30007.5, 0.01))

    def test_GivenMax_ReturnExpectedCountAndSampleRate(self):
        count, actual_sample_rate = self.AI.calculate_sample_rate_to_ticks(limits['sampleRate']['max'])

        self.assertEqual(count, 1333)
        self.assertEqual(actual_sample_rate, pytest.approx(30007.5, 0.01))

class Test_AnalogInput_CalculateCnfgValue(unittest.TestCase):
    def test_OpenAllChannelsForEachBank_HaveExpectedCnfgvalue(self):
        expectedResults = { 
            'channel': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'cnfgval': [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3]}

        def openAndCheck(bank):
            AI = AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                             {'bank': bank, 'channel': AIChannel.AI1},
                             {'bank': bank, 'channel': AIChannel.AI2},
                             {'bank': bank, 'channel': AIChannel.AI3},
                             {'bank': bank, 'channel': AIChannel.AI4},
                             {'bank': bank, 'channel': AIChannel.AI5},
                             {'bank': bank, 'channel': AIChannel.AI6},
                             {'bank': bank, 'channel': AIChannel.AI7},
                             {'bank': bank, 'channel': AIChannel.AI0, 'mode': AIMode.DIFFERENTIAL},
                             {'bank': bank, 'channel': AIChannel.AI1, 'mode': AIMode.DIFFERENTIAL},
                             {'bank': bank, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL},
                             {'bank': bank, 'channel': AIChannel.AI3, 'mode': AIMode.DIFFERENTIAL})
            AI.read()

            for index, channel_settings in enumerate(AI.channel_list):
                self.assertEqual(channel_settings['channel'], expectedResults['channel'][index])
                self.assertEqual(channel_settings['cnfgval'], expectedResults['cnfgval'][index])

            AI.close()

        openAndCheck(bankA)
        openAndCheck(bankB)

    def test_OpenTwoChannelsInBankAAndThreeChannelsInBankB_HaveExpectedCnfgvalue(self):
        expectedResults = [
            {'bank': 'A', 'channel': AIChannel.AI0, 'cnfgval': 8},
            {'bank': 'A', 'channel': AIChannel.AI5, 'cnfgval': 13},
            {'bank': 'B', 'channel': AIChannel.AI3, 'cnfgval': 11},
            {'bank': 'B', 'channel': AIChannel.AI2 + 8, 'cnfgval': 2},
            {'bank': 'B', 'channel': AIChannel.AI4, 'cnfgval': 12}]

        AI = AnalogInput({'bank': bankA, 'channel': AIChannel.AI0},
                         {'bank': bankB, 'channel': AIChannel.AI3},
                         {'bank': bankB, 'channel': AIChannel.AI2, 'mode': AIMode.DIFFERENTIAL},
                         {'bank': bankA, 'channel': AIChannel.AI5},
                         {'bank': bankB, 'channel': AIChannel.AI4})
        AI.read()

        for index, channel_settings in enumerate(AI.channel_list):
            self.assertEqual(channel_settings['bank'], expectedResults[index]['bank'])
            self.assertEqual(channel_settings['channel'], expectedResults[index]['channel'])
            self.assertEqual(channel_settings['cnfgval'], expectedResults[index]['cnfgval'])

        AI.close()

    def test_OpenFiveChannelsInBankAAndThreeChannelsInBankB_HaveExpectedCnfgvalue(self):
        expectedResults = [
            {'bank': 'A', 'channel': AIChannel.AI3 + 8, 'cnfgval': 3},
            {'bank': 'A', 'channel': AIChannel.AI7, 'cnfgval': 15},
            {'bank': 'A', 'channel': AIChannel.AI3, 'cnfgval': 11},
            {'bank': 'A', 'channel': AIChannel.AI0 + 8, 'cnfgval': 0},
            {'bank': 'A', 'channel': AIChannel.AI1 + 8, 'cnfgval': 1},
            {'bank': 'B', 'channel': AIChannel.AI3 + 8, 'cnfgval': 3},
            {'bank': 'B', 'channel': AIChannel.AI0, 'cnfgval': 8},
            {'bank': 'B', 'channel': AIChannel.AI4, 'cnfgval': 12}]

        AI = AnalogInput({'bank': bankA, 'channel': AIChannel.AI3, 'mode': AIMode.DIFFERENTIAL},
                         {'bank': bankB, 'channel': AIChannel.AI3, 'mode': AIMode.DIFFERENTIAL},
                         {'bank': bankB, 'channel': AIChannel.AI0},
                         {'bank': bankA, 'channel': AIChannel.AI7},
                         {'bank': bankA, 'channel': AIChannel.AI3},
                         {'bank': bankB, 'channel': AIChannel.AI4},
                         {'bank': bankA, 'channel': AIChannel.AI0, 'mode': AIMode.DIFFERENTIAL},
                         {'bank': bankA, 'channel': AIChannel.AI1, 'mode': AIMode.DIFFERENTIAL})
        AI.read()

        for index, channel_settings in enumerate(AI.channel_list):
            self.assertEqual(channel_settings['bank'], expectedResults[index]['bank'])
            self.assertEqual(channel_settings['channel'], expectedResults[index]['channel'])
            self.assertEqual(channel_settings['cnfgval'], expectedResults[index]['cnfgval'])

        AI.close()
