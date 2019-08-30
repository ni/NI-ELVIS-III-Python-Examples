"""
Hardware setup:
  1. Connect DIO15 to I2C.SDA of ADXL345.
  2. Connect DIO14 to I2C.SCL of ADXL345.
"""
import unittest
from nielvis import I2C, Bank, I2CSpeedMode

bank = Bank.A
slave_device_address = 0x53
data_to_write = [0x00, 0x80]
number_bytes_to_read = 1

class Test_I2C(unittest.TestCase):
    def test_readWithStandardMode(self):
        with I2C(bank, I2CSpeedMode.STANDARD) as I2C_standard_mode:  
            I2C_standard_mode.write(slave_device_address, data_to_write)
            
            return_value = I2C_standard_mode.read(slave_device_address, number_bytes_to_read)
            self.assertEqual(hex(return_value[0]), '0xe5')

    def test_readWithFastMode(self):
        with I2C(bank, I2CSpeedMode.FAST) as I2C_fast_mode:  
            I2C_fast_mode.write(slave_device_address, data_to_write)
            
            return_value = I2C_fast_mode.read(slave_device_address, number_bytes_to_read)
            self.assertEqual(hex(return_value[0]), '0xe5')
