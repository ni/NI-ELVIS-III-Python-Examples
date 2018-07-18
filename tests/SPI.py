"""
Hardware setup:
    1. Connect connector A SPI.CS(DIO0) to SPI.CS of ADXL345.
    2. Connect connector A SPI.CLK(DIO5) to SPI.CLK of ADXL345.
    3. Connect connector A SPI.MISO(DIO6) to SPI.MOSI of ADXL345.
    4. Connect connector A SPI.MOSI(DIO7) to SPI.MISO of ADXL345.
"""
import time
import academicIO
from enums import *

bank = Bank.A
frequency = 1000000     # 1MHz
frame_length = 8        # 1 byte
with academicIO.SPI(frequency, bank, SPIClockPhase.TRAILING, SPIClockPolarity.HIGH, SPIDataDirection.MSB, frame_length) as SPI:  
    # write and read
    SPI.write([0x80])
    value_array = SPI.read(1)
    print "value read from SPI.read: ", value_array[0]
    assert value_array[0] == 'e5'

    # writeread: an easier way to use write/read functions which will immediately read a value back right after the input value is written
    value_array = SPI.writeread([0x80])
    print "value read from SPI.writeread: ", value_array[0]
    assert value_array[0] == 'e5'

try:
    academicIO.SPI(frequency, bank, SPIClockPhase.TRAILING, SPIClockPolarity.HIGH, SPIDataDirection.MSB, 17)
except (AssertionError) as err:
    print "Caught the error - The frame length should be 4-16."

try:
    academicIO.SPI(frequency, bank, SPIClockPhase.TRAILING, SPIClockPolarity.HIGH, SPIDataDirection.MSB, 3)
except (AssertionError) as err:
    print "Caught the error - The frame length should be 4-16."