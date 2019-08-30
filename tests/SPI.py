"""
Hardware setup:
    1. Connect connector A SPI.CS(DIO0) to SPI.CS of ADXL345.
    2. Connect connector A SPI.CLK(DIO5) to SPI.CLK of ADXL345.
    3. Connect connector A SPI.MISO(DIO6) to SPI.MOSI of ADXL345.
    4. Connect connector A SPI.MOSI(DIO7) to SPI.MISO of ADXL345.
"""
import unittest
from nielvis import SPI, Bank, SPIClockPhase, SPIClockPolarity, SPIDataDirection, DIOChannel, DigitalInputOutput

bank = Bank.A
frequency = 1000000
frame_length = 8
clock_phase = SPIClockPhase.TRAILING
clock_polarity = SPIClockPolarity.HIGH
data_direction = SPIDataDirection.MSB

cs_channel = DIOChannel.DIO0

class Test_SPI(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cs = DigitalInputOutput(bank, [cs_channel])
        self.spi = SPI(frequency, bank, clock_phase, clock_polarity, data_direction, frame_length)

    @classmethod
    def tearDownClass(self):
        self.spi.close()
        self.cs.close()

    def __writeAndRead(self):
        self.cs.write(False, [cs_channel])

        self.spi.write([0x80])
        value_array = self.spi.read(1)

        self.cs.write(True, [cs_channel])
        return value_array

    def __writeread(self):
        self.cs.write(False, [cs_channel])

        value_array = self.spi.writeread([0x80])
        
        self.cs.write(True, [cs_channel])
        return value_array

    def test_WriteAndRead_ReturnExpectedReadback(self):
        value_array = self.__writeAndRead()
        self.assertEqual(value_array[0], 'e5')

    def test_WriteRead_ReturnExpectedReadback(self):
        value_array = self.__writeread()
        self.assertEqual(value_array[0], 'e5')

class Test_SPI_Assertion(unittest.TestCase):
    def test_OpenWithInvalidFrame_ShowAssertion(self):
        invalid_frame_lengthes = [3, 17]
        for invalid_frame_length in invalid_frame_lengthes:
            with self.assertRaises(AssertionError):
                SPI(frequency, bank, clock_phase, clock_polarity, data_direction, invalid_frame_length)
