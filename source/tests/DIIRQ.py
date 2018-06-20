"""
Output:
	The interrupt event occurs when a digital signal is inputed.
	The callback_function is called when the interrupt occured.
"""
import time
import academicIO
from enums import *

def irq_handler():
	print "DI interrupt is triggered. Now it is callback time."

irq_channel = DIIRQChannel.DIO1
with academicIO.DIIRQ(irq_channel) as DI_IRQ:
	irq_number = IRQNumber.IRQ2
	timeout= 6000
	interrupt_type_rising = True
	interrupt_type_falling = False
	edge_count = 1

	DI_IRQ.configure(irq_handler,
					 irq_number,
					 timeout,
					 interrupt_type_rising,
					 interrupt_type_falling,
					 edge_count)

	interrupt_type_rising = False
	interrupt_type_falling = True
	DI_IRQ.configure(irq_handler,
					 irq_number,
					 timeout,
					 interrupt_type_rising,
					 interrupt_type_falling,
					 edge_count)

	interrupt_type_rising = True
	interrupt_type_falling = True
	DI_IRQ.configure(irq_handler,
					 irq_number,
					 timeout,
					 interrupt_type_rising,
					 interrupt_type_falling,
					 edge_count)

	try:
		interrupt_type_rising = False
		interrupt_type_falling = False
		DI_IRQ.configure(irq_handler,
					 	irq_number,
					 	timeout,
					 	interrupt_type_rising,
					 	interrupt_type_falling,
					 	edge_count)
	except AssertionError:
		print "Caught the error - rising and falling interrupt type can't be false at the same time."

	try:
		DI_IRQ.configure(irq_handler,
						 0,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)
	except AssertionError:
		print "Caught the error - 0 can't be irq_number of DIIRQ."

	try:
		DI_IRQ.configure(irq_handler,
						 irq_number,
						 -1,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)
	except AssertionError:
		print "Caught the error - the timeout value should be greater than 0."

	try:
		DI_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 0)
	except AssertionError:
		print "Caught the error - the number of edges of the signal should be greater than 0."

	try:
		DI_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 4294967296)
	except AssertionError:
		print "Caught the error - the number of edges of the signal should be less than 4294967296."

irq_channel = 4
try:
	academicIO.DIIRQ(irq_channel)
except AssertionError:
	print "Caught the error - The channels available in the DIIRQ should be 0-3."