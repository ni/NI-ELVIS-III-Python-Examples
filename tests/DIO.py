"""
Hardware setup:
  1. Connect DIO2 and DIO9 on connector A.
  2. Connect DIO3 and DIO10 on connector A.
  1. Connect DIO4 and DIO11 on connector A.
  2. Connect DIO8 and DIO12 on connector A.
"""
import unittest
from nielvis import DigitalInputOutput, Bank, DIOChannel

bank = Bank.A

class Test_DigitalInputOuput(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.value = True
        self.dio = DigitalInputOutput(bank,
                                   [DIOChannel.DIO2, DIOChannel.DIO3, DIOChannel.DIO4, DIOChannel.DIO8,
                                    DIOChannel.DIO9, DIOChannel.DIO10, DIOChannel.DIO11, DIOChannel.DIO12])

    @classmethod
    def tearDownClass(self):
        self.dio.close()

    def test_WriteAndReadFourChannels(self):
        self.dio.write(self.value, [DIOChannel.DIO2, DIOChannel.DIO3, DIOChannel.DIO4, DIOChannel.DIO8])
        data = self.dio.read([DIOChannel.DIO9, DIOChannel.DIO10, DIOChannel.DIO11, DIOChannel.DIO12])
        self.assertEqual(data, [1, 1, 1, 1])

    def test_WriteAndReadTwoChannels(self):
        self.dio.write(self.value, [DIOChannel.DIO2, DIOChannel.DIO4])
        data = self.dio.read([DIOChannel.DIO9, DIOChannel.DIO11])
        self.assertEqual(data, [1, 1])

    def test_WriteAndReadSingleChannel(self):
        self.dio.write(not self.value, [DIOChannel.DIO3])
        data = self.dio.read([DIOChannel.DIO10])
        self.assertEqual(data, [0])

class Test_DigitalInputOuput_Assertion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.value = True
        self.channel = [DIOChannel.DIO1]
        self.dio = DigitalInputOutput(bank,
                                   [DIOChannel.DIO2, DIOChannel.DIO3, DIOChannel.DIO4, DIOChannel.DIO8,
                                    DIOChannel.DIO9, DIOChannel.DIO10, DIOChannel.DIO11, DIOChannel.DIO12])

    @classmethod
    def tearDownClass(self):
        self.dio.close()

    def test_writeInvalidValue_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.dio.write(200, self.channel)

    def test_writeInvalidChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.dio.write(self.value, [20])

    def test_readInvalidChannel_ShowAssertion(self):
        with self.assertRaises(AssertionError):
            self.dio.read([20])
