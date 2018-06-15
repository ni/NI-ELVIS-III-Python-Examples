"""
NI ELVIS III Serial Peripheral Interface (SPI) Example
This example illustrates how to write data to or read data from a SPI slave
device through the SPI channels on NI ELVIS III. An analog device which
support SPI is required. To create a SPI session you need to define six
parameters: frequency, bank, clock_phase, clock_polarity, data_direction, and
frame_length. Frequency and bank are requird parameters. The other parameters
are optional. The default values of the optional parameters are:
    clock_phase: 'Leading'
    clock_polarity: 'Low'
    data_direction: 'Most Significant Bit First'
    frame_length: 8

Hardware setup:
    1. Connect SPI.CS(DIO0) on bank A to SPI.CS of a slave device.
    2. Connect SPI.CLK(DIO5) on bank A to SPI.CLK of an slave device.
    3. Connect SPI.MISO(DIO6) on bank A to SPI.MOSI of an slave device.
    4. Connect SPI.MOSI(DIO7) on bank A to SPI.MISO of an slave device.

Output:
    SPI bus returns the a specified number of frames that SPI API reads from
    the SPI channel.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, SPIClockPhase, SPIClockPolarity, SPIDataDirection

# specify the SPI channel to which to write data to or read data from an SPI
# slave device
bank = Bank.A

# specify the frequency of the generated clock signal
frequency = 1000000    # 1MHz
# specify the clock phase at which the data remains stable in the SPI
# transmission cycle
clock_phase = SPIClockPhase.LEADING
# specify the base level of the clock signal and the logic level of the
# leading and trailing edges
clock_polarity = SPIClockPolarity.LOW
# specify the order in which the bits in the SPI frame are transmitted
data_direction = SPIDataDirection.MSB
# specify the number of bits that make up one SPI transmission frame
frame_length = 8   # 1 byte

# open an SPI session, and set initial values for the parameters
with NIELVISIIIAcademicIO.SPI(frequency,
                              bank,
                              clock_phase,
                              clock_polarity,
                              data_direction,
                              frame_length) as SPI:

    # The program reads values 20 times
    for x in range(0, 5):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)
        # write to slave device
        SPI.write([0x80])
        # read a 1 byte value from SPI channel
        value_array = SPI.read(1)
        # print the read back value
        print "value read from SPI.read: ", value_array[0]

        # writeread is an easier way to use write/read functions which will
        # immediately read a value back right after the input value is written
        value_array = SPI.writeread([0x80])
        # print the read back value
        print "value read from SPI.writeread: ", value_array[0]