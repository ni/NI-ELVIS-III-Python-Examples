"""
Hardware setup:
	1. Connect connector A UART.RX (DIO16) to UART.TX of a device.
	2. Connect connector A UART.TX (DIO17) to UART.RX of a device.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
baud_rate = UARTBaudRate.RATE9600
data_bits = UARTDataBits.BITS8
stop_bits = UARTStopBits.ONE
parity = UARTParity.NO
with academicIO.UART(bank,baud_rate, data_bits, stop_bits, parity) as uart:
    value = 'Hello World'
    uart.write(value)

    bytes_to_read = 10
    return_value = uart.read(bytes_to_read)
    print return_value