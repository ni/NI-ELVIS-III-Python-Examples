"""
Hardware setup:
    1. Connect AI0 and AO0 on connector A.
    2. Connect AI3 and AO1 on connector A.
    3. Connect AI0 and AO0 on connector B.
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

    def __start_thread(self, irq_thread):
        irq_thread.start()
        self.run = True
        
    def __close_thread(self, irq_thread):
        self.run = False
        irq_thread.join()

    def __reading_thread(self, read_object, number_of_samples, sample_rate, expected_value):
        value_array = None
        while self.run:
            value_array = read_object.read(number_of_samples, sample_rate)[0][0]

        values = [ round(value) for value in value_array ]
        print('%s should almost equal to %s' % (values, expected_value))

    def test_WriteSinglePoint_ReturnExpectedReadBack(self):
        input_value = 2.0       
        self.AO_single_channel.write(input_value)
        value_array = self.AI_single_channel.read()
        for value in value_array:
            self.assertEqual(value, pytest.approx(input_value, 0.1))

    def test_WriteSinglePoint_ReturnDifferentValueFromEachChannel(self):
        AO_multiple_channels = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                            {'bank': bank, 'channel': AOChannel.AO1})
        AI_multiple_channels = AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
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

    def test_WriteTensPointWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        sample_rate = 1000
        input_value = [1,1,2,2,3,3,4,4,5,5]
        expected_value = '1,1,2,2,3,3,4,4,5,5'
        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.AI_single_channel, len(input_value), sample_rate, expected_value))
        self.__start_thread(irq_thread)
        
        self.AO_single_channel.write(input_value, sample_rate)
        
        self.__close_thread(irq_thread)

    def test_WriteTenPointsThenWriteSinglePointInBankB_ReturnExpectedReadBack(self):
        AO0 = AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0})
        AI0 = AnalogInput({'bank': Bank.B, 'channel': AIChannel.AI0})

        def __multipleWriteAndRead():
            sample_rate = 1000
            input_value = [7,7,7,7,7,7,7,5,5,10]
            expected_value = '7,7,7,7,7,7,7,5,5,10'
            irq_thread = threading.Thread(target=self.__reading_thread, args=(AI0, len(input_value), sample_rate, expected_value))
            self.__start_thread(irq_thread)
            
            AO0.write(input_value, sample_rate)
            
            self.__close_thread(irq_thread)

        def __singleWriteAndRead():
            input_value = 3.2
            AO0.write(input_value)
            value = AI0.read()[0]

            self.assertEqual(value, pytest.approx(input_value, 0.1))
        
        __multipleWriteAndRead()
        __singleWriteAndRead()

        AO0.close()
        AI0.close()

    def test_OpenReadMultiplePointsCloseRepeatedly_DoesnotShowAnyError(self):
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
        

class Test_AnalogOutput_WriteTwoChannels(unittest.TestCase):
    def setUp(self):
        self.AO_multiple_channels = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                 {'bank': bank, 'channel': AOChannel.AO1})
        self.AI_multiple_channels = AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                                                {'bank': bank, 'channel': AIChannel.AI3})
    
    def tearDown(self):
        self.AO_multiple_channels.close()
        self.AI_multiple_channels.close()

    def __start_thread(self, irq_thread):
        irq_thread.start()
        self.run = True

    def __close_thread(self, irq_thread):
        self.run = False
        irq_thread.join()

    def __reading_thread(self, number_of_samples, sample_rate, expected_value):
        value_array = None
        while self.run:
            value_array = self.AI_multiple_channels.read(number_of_samples, sample_rate)

        value_array_in_bank_A = value_array[0]
        AI1_array = value_array_in_bank_A[0]
        AI3_array = value_array_in_bank_A[1]
        AI1_values = [ round(value) for value in AI1_array ]
        AI3_values = [ round(value) for value in AI3_array ]
        print('AO0 %s should almost equal to %s' % (AI1_values, expected_value))
        print('AO3 %s should almost equal to %s' % (AI3_values, expected_value))

    def test_WriteSinglePoint_ReturnExpectedReadBack(self):
        input_value = 3.5
        self.AO_multiple_channels.write(input_value)
        value_array = self.AI_multiple_channels.read()
        for value in value_array:
            self.assertEqual(value, pytest.approx(input_value, 0.1))

    def test_WriteSixteenPointsWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        sample_rate = 1000
        input_value = [9,9,9,9,9,9,9,9,9,9,5,5,5,2,2,2]
        expected_value = '9,9,9,9,9,9,9,9,9,9,5,5,5,2,2,2'
        irq_thread = threading.Thread(target=self.__reading_thread, args=(len(input_value), sample_rate, expected_value))
        self.__start_thread(irq_thread)
        
        self.AO_multiple_channels.write(input_value, sample_rate)
        
        self.__close_thread(irq_thread)


class Test_AnalogOutput_WriteSingleChannelContinuous(unittest.TestCase):
    def setUp(self):
        print()

    def __read(self, number_of_times_to_read, read_object, number_of_samples_to_read, timeout, expected_value):
        for i in range(0, number_of_times_to_read):
            value_array = read_object.read(number_of_samples_to_read, timeout)[0][0]
            values = [ round(value) for value in value_array ]
            print('continuous: %s should almost equal to %s and continuous from the last read' % (values, expected_value))

    def __start_thread(self, irq_thread):
        self.run_thread = True
        irq_thread.start()
        
    def __close_thread(self, irq_thread):
        self.run_thread = False
        irq_thread.join()

    def __writing_thread(self, write_object, input_value, timeout):
        while self.run_thread:
            write_object.write(input_value, timeout)

    def __convert_list_to_string(self, list):
        return ','.join(str(element) for element in list)

    def test_WriteSevenPointsWithTwoThousandSampleRateFromBankAThenCloseWithoutStop_ReturnExpectedReadBack(self):
        AO_single_channel = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
        AI_single_channel = AnalogInput({'bank': bank, 'channel': AIChannel.AI0})

        timeout = -1
        sample_rate = 2000
        input_value = [[9,8,7,6,5,4,3,2,1,0,9,8,7,6,5,4,3,2,1,0]]
        number_of_samples_to_read = 7
        expected_value = self.__convert_list_to_string(input_value)
        irq_thread = threading.Thread(target=self.__writing_thread, args=(AO_single_channel, input_value, timeout))
        
        AO_single_channel.start_continuous_mode(input_value, sample_rate, timeout)
        self.__start_thread(irq_thread)

        AI_single_channel.start_continuous_mode(sample_rate)
        
        self.__read(3, AI_single_channel, number_of_samples_to_read, timeout, expected_value)
            
        self.__close_thread(irq_thread)

        AO_single_channel.close()
        AI_single_channel.close()

    def test_WriteTenPointsWitOneThousandSampleRateFromBankBRepeatTwice_ReturnExpectedReadBack(self):
        def __write_and_read(input_value):
            AO_single_channel = AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0})
            AI_single_channel = AnalogInput({'bank': Bank.B, 'channel': AIChannel.AI0})

            timeout = -1
            sample_rate = 1000
            number_of_samples_to_read = 10
            expected_value = self.__convert_list_to_string(input_value)
            irq_thread = threading.Thread(target=self.__writing_thread, args=(AO_single_channel, input_value, timeout))
            
            AO_single_channel.start_continuous_mode(input_value, sample_rate, timeout)
            self.__start_thread(irq_thread)

            AI_single_channel.start_continuous_mode(sample_rate)
            
            self.__read(2, AI_single_channel, number_of_samples_to_read, timeout, expected_value)
                
            self.__close_thread(irq_thread)

            AO_single_channel.close()
            AI_single_channel.close()

        __write_and_read([[6,7,8,9,10,6,7,8,9,10,6,7,8,9,10]])
        __write_and_read([[0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]])


class Test_AnalogOutput_WriteTwoChannelsContinuous(unittest.TestCase):
    def setUp(self):
        print()

    def __start_thread(self, irq_thread):
        self.run_thread = True
        irq_thread.start()
        
    def __close_thread(self, irq_thread):
        self.run_thread = False
        irq_thread.join()

    def __writing_thread(self, write_object, input_value, timeout):
        while self.run_thread:
            write_object.write(input_value, timeout)

    def __convert_list_to_string(self, list):
        return ','.join(str(element) for element in list)

    def test_WriteToBankBAO1AndBankAAO0_ReturnExpectedReadBack(self):
        def __read(number_of_times_to_read, read_object, number_of_samples_to_read, timeout, expected_value_for_bank_A, expected_value_for_bank_B):
            result = [[], []]
            for i in range(0, number_of_times_to_read):
                value_array = read_object.read(number_of_samples_to_read, timeout)
                result[0].append(value_array[0])
                result[1].append(value_array[1])

            def __print(channels, expected_value):
                for channel in channels:
                    for values_per_channel in channel:
                        values = [ round(value) for value in values_per_channel ]
                        print('continuous: %s should almost equal to %s and continuous from the last read' % (values, expected_value))

            print('Bank A AI3 - AO1')
            __print(result[0], expected_value_for_bank_A)
            print('Bank B AI0 - AO0')
            __print(result[1], expected_value_for_bank_B)
        
        AO = AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0},
                          {'bank': bank, 'channel': AOChannel.AO1})
        AI = AnalogInput({'bank': Bank.B, 'channel': AIChannel.AI0},
                         {'bank': bank, 'channel': AIChannel.AI3})

        timeout = -1
        sample_rate = 1000
        input_value = [[1,2,3,4,5,6,7,8,9,10], [10,9,8,7,6,5,4,3,2,1]]
        number_of_samples_to_read = 5
        expected_value_for_bank_B = self.__convert_list_to_string(input_value[0])
        expected_value_for_bank_A = self.__convert_list_to_string(input_value[1])
        irq_thread = threading.Thread(target=self.__writing_thread, args=(AO, input_value, timeout))
        
        AO.start_continuous_mode(input_value, sample_rate, timeout)
        self.__start_thread(irq_thread)

        AI.start_continuous_mode(sample_rate)
        
        __read(2, AI, number_of_samples_to_read, timeout, expected_value_for_bank_A, expected_value_for_bank_B)
            
        self.__close_thread(irq_thread)

        AO.close()
        AI.close()

    def test_WriteToBankAAO0andAO1_ReturnExpectedReadBack(self):
        def __read(number_of_times_to_read, read_object, number_of_samples_to_read, timeout, expected_value_for_AI0, expected_value_for_AI3):
            result = [[], []]
            for i in range(0, number_of_times_to_read):
                value_array = read_object.read(number_of_samples_to_read, timeout)[0]
                result[0].append(value_array[0])
                result[1].append(value_array[1])

            def __print(channels, expected_value):
                for values in channels:
                    values = [ round(value) for value in values ]
                    print('continuous: %s should almost equal to %s and continuous from the last read' % (values, expected_value))

            print('Bank A AI0 - AO0')
            __print(result[0], expected_value_for_AI0)
            print('Bank A AI3 - AO1')
            __print(result[1], expected_value_for_AI3)
        
        AO = AnalogOutput({'bank': bank, 'channel': AOChannel.AO0},
                          {'bank': bank, 'channel': AOChannel.AO1})
        AI = AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
                         {'bank': bank, 'channel': AIChannel.AI3})

        timeout = -1
        sample_rate = 1000
        input_value = [[1,1,2,2,3,3,4,4,5,5,1,1,2,2,3,3,4,4,5,5], [6,6,7,7,8,8,9,9,10,10,6,6,7,7,8,8,9,9,10,10]]
        number_of_samples_to_read = 5
        expected_value_for_AI0 = self.__convert_list_to_string(input_value[0])
        expected_value_for_AI3 = self.__convert_list_to_string(input_value[1])
        irq_thread = threading.Thread(target=self.__writing_thread, args=(AO, input_value, timeout))
        
        AO.start_continuous_mode(input_value, sample_rate, timeout)
        self.__start_thread(irq_thread)

        AI.start_continuous_mode(sample_rate)
        
        __read(2, AI, number_of_samples_to_read, timeout, expected_value_for_AI0, expected_value_for_AI3)
            
        self.__close_thread(irq_thread)

        AO.close()
        AI.close()

    def test_WriteToBankBAO1AndBankAAO0AO1WithDifferentValuesLength_ReturnExpectedReadBack(self):
        def __read(number_of_times_to_read, read_object, number_of_samples_to_read, timeout, expected_value):
            # result = [A: [AO0, AO1], B: [AO0]]
            result = [[[],[]], [[],[]]]
            for i in range(0, number_of_times_to_read):
                value_array = read_object.read(number_of_samples_to_read, timeout)
                bank_A_values = value_array[0]
                bank_B_values = value_array[1]
                result[0][0].append(bank_A_values[0])
                result[0][1].append(bank_A_values[1])
                result[1][0].append(bank_B_values[0])

            def __print(channels, bank):
                for channel in channels:
                    for index, values_per_channel in enumerate(channel):
                        values = [ round(value) for value in values_per_channel ]
                        if bank == Bank.A.value:
                            print('continuous: %s should almost equal to %s and continuous from the last read' % (values, expected_value[index]))
                        else:
                            print('continuous: %s should almost equal to %s and continuous from the last read' % (values, expected_value[2]))

            print('Bank A')
            __print(result[0], Bank.A.value)
            print('Bank B')
            __print(result[1], Bank.B.value)
        
        AO = AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0},
                          {'bank': bank, 'channel': AOChannel.AO0},
                          {'bank': bank, 'channel': AOChannel.AO1})
        AI = AnalogInput({'bank': Bank.B, 'channel': AIChannel.AI0},
                         {'bank': bank, 'channel': AIChannel.AI0},
                         {'bank': bank, 'channel': AIChannel.AI3})

        timeout = -1
        sample_rate = 1000
        input_value = [[0,1,2,3,4,5,0,1,2,3,4,5], [7,8,9,10,7,8,9,10,7,8,9,10], [1,2,3,4,5,1,2,3,4,5]]
        number_of_samples_to_read = 4
        expected_value = [self.__convert_list_to_string(input_value[1]), self.__convert_list_to_string(input_value[2]), self.__convert_list_to_string(input_value[0])]
        irq_thread = threading.Thread(target=self.__writing_thread, args=(AO, input_value, timeout))
        
        AO.start_continuous_mode(input_value, sample_rate, timeout)
        self.__start_thread(irq_thread)
        
        AI.start_continuous_mode(sample_rate)
        
        __read(2, AI, number_of_samples_to_read, timeout, expected_value)
        
        self.__close_thread(irq_thread)

        AO.close()
        AI.close()


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

    def tearDown(self):
        self.AO_single_channel.close()

    def test_PassInvalidInputValues_ShowAssertion(self):
        wrong_values = [0, [], [[]]]

        for wrong_value in wrong_values:
            with self.assertRaises(AssertionError):
                self.AO_single_channel.start_continuous_mode(wrong_value, self.expectedSampleRate, self.expectedTimeout)
                
    def test_PassInvalidSampleRateToSingleChannel_ShowAssertion(self):
        limits = {'SampleRate': {'min': 1000, 'max': 1600000}}
        wrong_sample_rates = [limits['SampleRate']['min'] - 1, limits['SampleRate']['max'] + 1]

        for wrong_sample_rate in wrong_sample_rates:
            with self.assertRaises(AssertionError):
                self.AO_single_channel.start_continuous_mode(self.expectedInput, wrong_sample_rate, self.expectedTimeout)
