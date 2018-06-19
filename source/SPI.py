"""
NI ELVIS III Serial Peripheral Interface (SPI) Example
This example illustrates how to write data to or read data from an SPI slave
device through the SPI channels on the NI ELVIS III. To create an SPI session,
you need to define six parameters: frequency, bank, clock_phase,
clock_polarity, data_direction, and frame_length. frequency and bank are
required parameters. The other parameters are optional. The default values of
the optional parameters are:
    clock_phase: LEADING
    clock_polarity: LOW
    data_direction: MSB
    frame_length: 8

Hardware setup:
    1. Connect SPI.CS(DIO0) on bank A to SPI.CS of a slave device.
    2. Connect SPI.CLK(DIO5) on bank A to SPI.CLK of a slave device.
    3. Connect SPI.MISO(DIO6) on bank A to SPI.MOSI of a slave device.
    4. Connect SPI.MOSI(DIO7) on bank A to SPI.MISO of a slave device.

Result:
    The program reads a specified number of frames from the SPI channel.
"""
import time
import academicIO
from enums import Bank, SPIClockPhase, SPIClockPolarity, SPIDataDirection

# specify the bank
bank = Bank.A

# specify the frequency, in Hz, of the generated clock signal
frequency = 1000000
# specify the clock phase at which the data remains stable in the SPI
# transmission cycle
clock_phase = SPIClockPhase.LEADING
# specify the base level of the clock signal and the logic level of the
# leading and trailing edges
clock_polarity = SPIClockPolarity.LOW
# specify the order in which the bits in the SPI frame are transmitted
data_direction = SPIDataDirection.MSB
# specify the number of bits that make up one SPI transmission frame
frame_length = 8

# open an SPI session, and set initial values for the parameters
with academicIO.SPI(frequency,
                              bank,
                              clock_phase,
                              clock_polarity,
                              data_direction,
                              frame_length) as SPI:

    # The program writes and reads values 5 times
    for x in range(0, 5):
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)
        # specify the bytes to read from the SPI channel
        SPI.write([0x80])
        # specify the number of frame to read from the SPI channel
        number_frames = 1
        # read a 1 byte data from SPI channel
        value_array = SPI.read(number_frames)
        # print the data
        print "value read from SPI.read: ", value_array[0]

        # You can also choose the writeread function which reads back a value
        # immediately after it is written
        value_array = SPI.writeread([0x80])
        # print the data read back from the SPI channel
        print "value read from SPI.writeread: ", value_array[0]