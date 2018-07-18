"""
NI ELVIS III Inter-Integrated Circuit (I2C) Example
This example illustrates how to write data to or read data from an I2C slave
device through the I2C channels. The program first defines the configuration
for the I2C communication, then writes to and reads from the I2C device in a
loop. Each time the write is called a list of hexadecimal data is written to
the I2C device; each time the read is called a list of data is returned from
the I2C device.

The I2C configuration consists of two parameters: bank and mode. There are two
identical banks of I2C port (A and B). There are two speeds of I2C
communication (standard and fast).

To read data from and write data to the I2C slave device, you must specify an
address in 7 bits. Some I2C devices might have an 8-bit address in which the
first 7 bits represent the address and the last bit represents the mode of
operation. For this kind of I2C devices, you must specify the slave address
(7-bit) using the seven most significant bits (MSB). For example, a device
provides a 8-bit slave address 10100110. You can determine it to '1010011 0'
which has a 7-bit slave address 1010011. The last bit (0) is used to determine
either to write to the slave device or read from the slave device. The NI
ELVIS III helper library (academicIO) will insert the read/write bit based on
the function been called.

See https://www.nxp.com/docs/en/user-guide/UM10204.pdf for more details about
I2C.

slave_device_address is an address which refers to the slave device. The slave
device address is 0x53 which specifies to a 7-bit I2C connection address of
ADXL345. You might need to change the slave device address depends on the
device you have. This example illustrates how to set the ADXL345 device to
measure mode by setting the power control register (0x2D).

See http://www.analog.com/media/en/technical-documentation/data-sheets/ADXL345.pdf
for more details about ADXL345. See page.25 for more details about power
control register.

This example uses:
    1. Bank A, Channel DIO14.
    2. Bank A, Channel DIO15.

Hardware setup:
    1. Connect an I2C.SCL of a slave device to I2C.SCL (DIO14) on bank A.
    2. Connect an I2C.SDA of a slave device to I2C.SDA (DIO15) on bank A.

Result:
    The program sets the I2C device to measure mode and reads a value from the
    I2C slave device. The slave device returns the value that just be written
    into the register. The returned value is 8 in decimal.
"""
import time
import academicIO
from enums import Bank, I2CSpeedMode

# specify the bank
bank = Bank.A
# specify the mode of operation that this program uses to communicate with the
# I2C slave device
speed = I2CSpeedMode.STANDARD

# open an I2C session
with academicIO.I2C(bank, speed) as I2C:
    # specify the address, in hexadecimal, using the seven most significant
    # bits (MSB) of the I2C slave device
    slave_device_address = 0x53

    # specify the bytes to write to the I2C slave device
    # the first parameter of the write function is 0x2D which represents to
    # the power control register of ADXL345, and the second parameter of the
    # write function is the value to write to the register. 0x08 sets the
    # third bit of the power control register to high which sets the device to
    # measure mode.
    data_to_write = [0x2D, 0x08]
    # write data to the I2C slave device
    I2C.write(slave_device_address, data_to_write)

    # specify the number of bytes to read from the I2C slave device
    number_bytes_to_read = 1
    # read data from the I2C slave device
    return_value = I2C.read(slave_device_address, number_bytes_to_read)
    # print the data
    print return_value
