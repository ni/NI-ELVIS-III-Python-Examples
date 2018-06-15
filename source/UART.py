"""
NI ELVIS III Universal Asynchronous Receiver/Transmitter (UART) Example
This example illustrates how to wrties data to or read data from a UART device
through the UART channels. on NI ELVIS III. To create an UART session, you
need to define one required parameter: bank.
To configure the UART VISA, you need to define four parameters: baud rate,
data bits, stop bits , and parity. The default values of these parameters are:
    baud_rate: 9600
    data_bits: 8
    stop_bits: 10
    parity: 0

Hardware setup:
    1. Connect UART.RX (DIO16) on bank A to UART.TX of a device.
    2. Connect UART.TX (DIO17) on bank A to UART.RX of a device.

Output:
    'Hello World' is written to the UART device and a one bytes value is read
    from the device through the UART channels.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Bank, UARTBaudRate, UARTDataBits, UARTParity, UARTStopBits

bank = Bank.A
# open an UART session, and set initial values for the parameters
with NIELVISIIIAcademicIO.UART(bank) as uart:
    # specify the baud rate, data bits, stop bits, and parity for the UART
    # session:
    #     baud rate = 9600
    #     data bits = 8
    #     stop bits = one
    #     parity = none
    baud_rate = UARTBaudRate.RATE9600
    data_bits = UARTDataBits.BITS8
    stop_bits = UARTStopBits.ONE
    parity = UARTParity.NO

    # configure the UART VISA
    uart.configure(baud_rate,
                   data_bits,
                   stop_bits,
                   parity)

    # specify the data to write to the UART device
    value = 'Hello World'
    # write data to the UART device
    uart.write(value)

    # specify bytes of data to read from the UART device
    bytes_to_read = 1
    # The program reads values 20 times
    for x in range(0, 20):
        # read a one btye data from the UART device
        return_value = uart.read(bytes_to_read)
        # print the data read from UART device
        print return_value
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)
