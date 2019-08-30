"""
Use DIO to test the SysSelect Calculation
"""
import unittest
from nielvis import DigitalInputOutput, Bank, DIOChannel

channel3 = 3
channel16 = 16
number_of_channels_to_write_2 = 2
number_of_channels_to_write_3 = 3

class Test_SysSelect32BitCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.dio = DigitalInputOutput(Bank.A, [DIOChannel.DIO0])
        self.expectedRegisterValue = {
            '0xAAAAAAAA': 0b10101010101010101010100000101010,
            '0xFFFFFFFF': 0b11111111111111111111110000111111,
        }

    @classmethod
    def tearDownClass(self):
        self.dio.close()
        
    def test_ClearChannel3With0xAAAAAAAA_ReturnExpectedValue(self):
        expectedRegisterValue = self.expectedRegisterValue['0xAAAAAAAA']
        result = self.dio.clear_sys_select(0xAAAAAAAA, channel3, number_of_channels_to_write_2)
        self.assertEqual(result, expectedRegisterValue)

    def test_SetChannel3With0xAAAAAAAA_ReturnExpectedValue(self):
        expectedRegisterValue = 0b10101010101010101010100101101010
        result = self.dio.set_sys_select(self.expectedRegisterValue['0xAAAAAAAA'], channel3, number_of_channels_to_write_2, '01')
        self.assertEqual(result, expectedRegisterValue)
        
    def test_ClearChannel3With0xFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = self.expectedRegisterValue['0xFFFFFFFF']
        result = self.dio.clear_sys_select(0xFFFFFFFF, channel3, number_of_channels_to_write_2)
        self.assertEqual(result, expectedRegisterValue)

    def test_SetChannel3With0xFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = 0b11111111111111111111110101111111
        result = self.dio.set_sys_select(self.expectedRegisterValue['0xFFFFFFFF'], channel3, number_of_channels_to_write_2, '01')
        self.assertEqual(result, expectedRegisterValue)

class Test_SysSelect64BitCalculation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.dio = DigitalInputOutput(Bank.A, [DIOChannel.DIO0])
        self.expectedRegisterValue = {
            'channel3': 0b1111111111111111111111111111111111111111111111111111110000111111,
            'channel16': 0b1111111111111111111111111100000011111111111111111111111111111111,
        }

    @classmethod
    def tearDownClass(self):
        self.dio.close()
        
    def test_ClearChannel3With0xFFFFFFFFFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = self.expectedRegisterValue['channel3']
        result = self.dio.clear_sys_select(0xFFFFFFFFFFFFFFFF, channel3, number_of_channels_to_write_2)
        self.assertEqual(result, expectedRegisterValue)

    def test_SetChannel3With0xFFFFFFFFFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = 0b1111111111111111111111111111111111111111111111111111110101111111
        result = self.dio.set_sys_select(self.expectedRegisterValue['channel3'], channel3, number_of_channels_to_write_2, '01')
        self.assertEqual(result, expectedRegisterValue)

    def test_ClearChannel16With0xFFFFFFFFFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = self.expectedRegisterValue['channel16']
        result = self.dio.clear_sys_select(0xFFFFFFFFFFFFFFFF, channel16, number_of_channels_to_write_3)
        self.assertEqual(result, expectedRegisterValue)

    def test_SetChannel16With0xFFFFFFFFFFFFFFFF_ReturnExpectedValue(self):
        expectedRegisterValue = 0b1111111111111111111111111110101011111111111111111111111111111111
        result = self.dio.set_sys_select(self.expectedRegisterValue['channel16'], channel16, number_of_channels_to_write_3, '10')
        self.assertEqual(result, expectedRegisterValue)
