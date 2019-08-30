"""
Use GY25 chip.
Hardware setup:
	1. Connect connector A UART.RX (DIO16) to UART.TX of a device.
	2. Connect connector A UART.TX (DIO17) to UART.RX of a device.
"""
import time
import unittest
from nielvis import UART, Bank, UARTBaudRate, UARTDataBits, UARTStopBits, UARTParity

bank = Bank.A
baud_rate = UARTBaudRate.RATE115200
data_bits = UARTDataBits.BITS8
stop_bits = UARTStopBits.ONE
parity = UARTParity.NO

class Test_UART(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.uart = UART(bank,baud_rate, data_bits, stop_bits, parity)

    @classmethod
    def tearDownClass(self):
        self.uart.close()

    def test_WriteAndRead1Byte_ReturnExpectedValue(self):
        self.uart.write(b'\xA5')
        self.uart.write(b'\x51')
        time.sleep(0.1)

        bytes_to_read = 1
        return_value = self.uart.read(bytes_to_read)
        self.assertEqual(return_value, b'\xAA')
