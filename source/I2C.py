"""
NI ELVIS III Inter-Integrated Circuit (I2C) Example
This example illustrates how to write data to or read data from an I2C slave
device through the I2C channels. To create an I2C session, you need to define
two required parameters, bank and mode. To read data from and write data to
the I2C slave device, you must specify an address in 7 bits. Some I2C devices
might have an 8-bit address in which the first 7 bits represent the address
and the last bit represents the mode of operation. For this kind of I2C
devices, you must specify the slave address(7-bit) using the seven most
significant bits.

slave_device_address is an address which refers to the slave device. In this
example, slave_device_address is 0x53 which specifies to the I2C connection
address of ADXL345. You might need to change the slave_device_address depends
on the device you have.

Hardware setup:
    1. Connect an I2C.SCL of a slave device to DIO14 on bank A.
    2. Connect an I2C.SDA of a slave device to DIO15 on bank A.

Result:
    The program reads values from the I2C slave device.
"""
import time
import academicIO
from enums import Bank, I2CSpeedMode

# specify the bank
bank = Bank.A
# specify the mode of operation that this program uses to communicate with the
# I2C slave device
speed = I2CSpeedMode.STANDARD

# open an I2C session, and set initial values for the parameters
with academicIO.I2C(bank, speed) as I2C:
    # specify the address of the I2C slave device
    slave_device_address = 0x53

    # The program reads values 5 times
    for i in range(0, 5):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # specify the bytes to write to the I2C slave device
        data_to_write = [0x00, 0x80]
        # write data to the I2C slave device
        I2C.write(slave_device_address, data_to_write)

        # specify the number of bytes to read from the I2C slave device
        number_bytes_to_read = 1
        # read data from the I2C slave device
        return_value = I2C.read(slave_device_address, number_bytes_to_read)
        # print the data
        print return_value