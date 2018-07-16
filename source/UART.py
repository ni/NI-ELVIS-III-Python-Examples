"""
NI ELVIS III Universal Asynchronous Receiver/Transmitter (UART) Example
This example illustrates how to write data to or read data from an Universal
Asynchronous Receiver/Transmitter (UART) device through the UART channels on
the NI ELVIS III. The program first defined the configuration for the UART
communication, then writes to and reads from the UART device in a loop. Each
time the write is called a string is returned from the UART device; each time
the read is called a string is returned from the UART device.

The UART configuration consists of one parameter: bank, and there are two
identical banks of AI channels (A and B).

The UART configure function consists five parameters: baud rate (110, 300, 600,
1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, and 230400), data bits (7
and 8), stop bits (one and two), parity (none, odd, and even), and
flow_control (none, xor and xoff, rts and cts, and dtr and dsr).

This example illustrates how to write to and read from a UART device, FTDI232.
See http://www.ftdichip.com/Documents/DataSheets/ICs/DS_FT232R.pdf for more
details.

This example uses:
    1. Bank A, Channel DIO16.
    2. Bank A, Channel DIO17.

Hardware setup:
    1. Connect UART.RX (DIO16) on bank A to UART.TX of a UART device.
    2. Connect UART.TX (DIO17) on bank A to UART.RX of a UART device.

Result:
    The program writes a string 'Hello World' to the UART device, and
    reads five bytes of data from the device.
"""
import time
import academicIO
from enums import Bank, UARTBaudRate, UARTDataBits, UARTParity, UARTStopBits, UARTFlowControl

# specify the bank
bank = Bank.A
# open a UART session
with academicIO.UART(bank) as uart:
    # specifies the baud rate of transmission
    baud_rate = UARTBaudRate.RATE9600
    # specifies the number of bits in the incoming data
    data_bits = UARTDataBits.BITS8
    # specifies the number of stop bits this program uses to indicate the end
    # of a data
    stop_bits = UARTStopBits.ONE
    # specifies the parity bits to write or read characters
    parity = UARTParity.NO
    # sets the type of control used by the transfer mechanism
    flow_control = UARTFlowControl.NONE

    # configure the UART VISA
    uart.configure(baud_rate,
                   data_bits,
                   stop_bits,
                   parity,
                   flow_control)

    # specify the data to write to the UART device
    value = 'Hello World'
    # write the data to the UART device
    uart.write(value)

    # specify the number of bytes to read from the device
    bytes_to_read = 5
    # read five bytes of data from the device
    return_value = uart.read(bytes_to_read)
    # print the data read from the UART device
    print return_value
