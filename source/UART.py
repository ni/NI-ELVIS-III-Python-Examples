"""
NI ELVIS III Universal Asynchronous Receiver/Transmitter (UART) Example
This example illustrates how to write data to or read data from a UART device
through the UART channels on the NI ELVIS III. To create a UART session, you
need to define bank, which is a required parameter, bank. To configure the
UART communication, you need to define five parameters: baud rate, data bits,
stop bits, parity, and flow control. The default values of these parameters are:
    baud_rate: RATE9600
    data_bits: BITS8
    stop_bits: ONE
    parity: NO
    flow_control = NONE

Hardware setup:
    1. Connect UART.RX (DIO16) on bank A to UART.TX of a UART device.
    2. Connect UART.TX (DIO17) on bank A to UART.RX of a UART device.

Result:
    The program writes a string to the UART device and reads one byte of data
    from the device.
"""
import time
import academicIO
from enums import Bank, UARTBaudRate, UARTDataBits, UARTParity, UARTStopBits, UARTFlowControl

# specify the bank
bank = Bank.A
# open a UART session, and set initial values for the parameters
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
    bytes_to_read = 1
    # The program reads values 20 times
    for x in range(0, 20):
        # read one byte of data from the device
        return_value = uart.read(bytes_to_read)
        # print the data read from the UART device
        print return_value
        # delay for 0.001 seconds so that the program does not run too fast
        time.sleep(0.001)
