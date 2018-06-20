"""
Output:
	The interrupt event occurs when the button is clicked; otherwise timeout.
	The callback_function function is called when the interrupt occured.
"""					 
import time
import academicIO
from enums import *

def irq_handler():
	print "Button interrupt is triggered. Now it is callback time."

with academicIO.ButtonIRQ() as Button_IRQ:
	irq_number = IRQNumber.IRQ1
	timeout= 6000
	interrupt_type_rising = True
	interrupt_type_falling = False
	edge_count = 2
	Button_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)

	interrupt_type_rising = False
	interrupt_type_falling = True
	Button_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)

	interrupt_type_rising = True
	interrupt_type_falling = True
	Button_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)

	try:
		interrupt_type_rising = False
		interrupt_type_falling = False
		Button_IRQ.configure(irq_handler,
						 	irq_number,
						 	timeout,
						 	interrupt_type_rising,
						 	interrupt_type_falling,
						 	edge_count)
	except AssertionError:
		print "Caught the error - rising and falling interrupt type can't be false at the same time."

	try:
		Button_IRQ.configure(irq_handler,
							0,
							timeout,
							interrupt_type_rising,
							interrupt_type_falling,
							edge_count)
	except AssertionError:
		print "Caught the error - 0 can't be irq_number of ButtonIRQ."

	try:
		Button_IRQ.configure(irq_handler,
							irq_number,
							-1,
							interrupt_type_rising,
							interrupt_type_falling,
							edge_count)
	except AssertionError:
		print "Caught the error - the timeout value should be greater than 0."

	try:
		Button_IRQ.configure(irq_handler,
							irq_number,
							timeout,
							interrupt_type_rising,
							interrupt_type_falling,
							0)
	except AssertionError:
		print "Caught the error - the number of edges of the signal should be greater than 0."

	try:
		Button_IRQ.configure(irq_handler,
							irq_number,
							timeout,
							interrupt_type_rising,
							interrupt_type_falling,
							4294967296)
	except AssertionError:
		print "Caught the error - the number of edges of the signal should be less than 4294967296."