"""
NI ELVIS III Inter-Integrated Circuit (I2C) Example
This example illustrates how to writes data to or reads data from an I2C slave
device through the I2C channels. To create an AI session, you need to define
two required parameters: bank and mode. To read and write to the I2C slave
device, you must specify an address in 7 bits. Some I2C devices might have an
8-bit address in which the first 7 bits represent the address and the last bit
represents the mode of operation. For this kind of I2C devices, you must
specify Slave Address (7-bit) using the seven most significant bits.

Hardware setup:
    1. Connect an I2C.SCL of a slave device to DIO14 on bank A.
    2. Connect an I2C.SDA of a slave device to DIO15 on bank A.

Output:
    The program reads values from the I2C slave device.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, I2CSpeedMode

# specify the I2C bank to which to wrtie data to and read data from the I2C
# slave device
bank = Bank.A
# specify the mode of operation that this example uses to communicate with the
# I2C slave device
speed = I2CSpeedMode.STANDARD

# open an I2C session, and set initial values for the parameters
with NIELVISIIIAcademicIO.I2C(bank, speed) as I2C:
    # specify the address of the I2C slave device which this example reads data
    # from or writes data to
    slave_device_address = 0x53

    # The program reads values 5 times
    for i in range(0, 5):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)

        # specify the data bytes to write to the I2C slave device
        data_to_write = [0x00, 0x80]
        # write data to the I2C slave device
        I2C.write(slave_device_address, data_to_write)

        # specify the number of bytes to read from the I2C slave device
        number_bytes_to_read = 1
        # read data from the I2C slave device
        return_value = I2C.read(slave_device_address, number_bytes_to_read)
        # print the data
        print return_value