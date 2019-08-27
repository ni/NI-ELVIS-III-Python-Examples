"""
Output:
    The interrupt event occurs when a digital signal is inputed.
    The callback_function is called when the interrupt occured.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

def irq_handler():
    print("DI interrupt is triggered. Now it is callback time.")

irq_channel = DIIRQChannel.DIO1

irq_number = IRQNumber.IRQ2
timeout= 6000
interrupt_type_rising = True
interrupt_type_falling = False
edge_count = 1
with academicIO.DIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      interrupt_type_rising,
                      interrupt_type_falling,
                      edge_count) as DI_IRQ:
    DI_IRQ.wait()

interrupt_type_rising = False
interrupt_type_falling = True
with academicIO.DIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      interrupt_type_rising,
                      interrupt_type_falling,
                      edge_count) as DI_IRQ:
    DI_IRQ.wait()

interrupt_type_rising = True
interrupt_type_falling = True
with academicIO.DIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      interrupt_type_rising,
                      interrupt_type_falling,
                      edge_count) as DI_IRQ:
    DI_IRQ.wait()

interrupt_type_rising = False
interrupt_type_falling = False
try:
    academicIO.DIIRQ(irq_channel,
                     irq_handler,
                     irq_number,
                     timeout,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     edge_count)
except AssertionError:
    print("Caught the error - rising and falling interrupt type can't be false at the same time.")

try:
    academicIO.DIIRQ(irq_channel,
                     irq_handler,
                     0,
                     timeout,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     edge_count)
except AssertionError:
    print("Caught the error - 0 can't be irq_number of DIIRQ.")

try:
    academicIO.DIIRQ(irq_channel,
                     irq_handler,
                     irq_number,
                        -1,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     edge_count)
except AssertionError:
    print("Caught the error - the timeout value should be greater than 0.")

try:
    academicIO.DIIRQ(irq_channel,
                     irq_handler,
                     irq_number,
                        timeout,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     0)
except AssertionError:
    print("Caught the error - the number of edges of the signal should be greater than 0.")

try:
    academicIO.DIIRQ(irq_channel,
                     irq_handler,
                     irq_number,
                        timeout,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     4294967296)
except AssertionError:
    print("Caught the error - the number of edges of the signal should be less than 4294967296.")

try:
    academicIO.DIIRQ(4,
                     irq_handler,
                     irq_number,
                     timeout,
                     interrupt_type_rising,
                     interrupt_type_falling,
                     edge_count)
except AssertionError:
    print("Caught the error - The channels available in the DIIRQ should be 0-3.")