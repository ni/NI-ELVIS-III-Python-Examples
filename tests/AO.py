"""
Hardware setup:
    1. Connect AI0 and AO0 on connector A.
    2. Connect AI3 and AO1 on connector A.
"""
import unittest
import time
import pytest
import threading
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
limits = { 'sampleRate': { 'min': 1, 'max': 1600000}}

class Test_AnalogOutput_WriteSingleChannel(unittest.TestCase):
    def setUp(self):
        self.AO_single_channel = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})
        self.AI_single_channel = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0})

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

    def test_WriteTensPointWithOneThousandSampleRate_ReturnExpectedReadBack(self):
        sample_rate = 1000
        input_value = [1,1,2,2,3,3,4,4,5,5]
        expected_value = '1,1,2,2,3,3,4,4,5,5'
        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.AI_single_channel, len(input_value), sample_rate, expected_value))
        self.__start_thread(irq_thread)
        
        self.AO_single_channel.write(input_value, sample_rate)
        
        self.__close_thread(irq_thread)

    def test_WriteTenPointsThenWriteSinglePointInBankB_ReturnExpectedReadBack(self):
        AO0 = academicIO.AnalogOutput({'bank': Bank.B, 'channel': AOChannel.AO0})
        AI0 = academicIO.AnalogInput({'bank': Bank.B, 'channel': AIChannel.AI0})

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


class Test_AnalogOutput_WriteTwoChannels(unittest.TestCase):
    def setUp(self):
        self.AO_multiple_channels = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0}, 
                                                            {'bank': bank, 'channel': AOChannel.AO1})
        self.AI_multiple_channels = academicIO.AnalogInput({'bank': bank, 'channel': AIChannel.AI0},
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

class Test_AnalogOutput_OpenAssertion(unittest.TestCase):
    def test_OpenWithInvalidBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogOutput({'bank': 'C', 'channel': AOChannel.AO0})

    def test_OpenWithInvalidChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogOutput({'bank': bank, 'channel': 2})

    def test_OpenWithoutBank_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogOutput({'channel': AOChannel.AO0})

    def test_OpenWithoutChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            academicIO.AnalogOutput({'bank': bank})


class Test_AnalogOutput_WriteAssertion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.AO = academicIO.AnalogOutput({'bank': bank, 'channel': AOChannel.AO0})

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