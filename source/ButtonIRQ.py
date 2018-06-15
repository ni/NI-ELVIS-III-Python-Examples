"""
NI ELVIS III Button Interrupt (ButtonIRQ) Example
This example illustrates how to trigger an ButtonIRQ on NI ELVIS III. To
configure and wait on an interrupt triggered, you need to define six
parameters: irq_handler, irq_number, timeout, interrupt_type_rising,
interrupt_type_falling, and edge_count. You must use callback function to
handle interrupt. The callback function contains code that handles interrupts
and runs when the interrupts triggering occurs. The other parameters are
optional. The default values of the optional parameters are:
    irq_number: 1
	timeout: 10000
	interrupt_type_rising: True
	interrupt_type_falling: False
	edge_count: 1

Note: irq_number refers to the irq number of this interrupt event. The valid
values are within the range [1:7]. You cannot register an I/O interrupt with
the same IRQ number as a registered I/O interrupt. However, after you closed
the existing interrupt, you can use the IRQ number to register another
interrupt.

Output:
    The interrupt event occurs when the button is clicked.
    The irq_handler function is called when the interrupt is triggered.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import IRQNumber, Led

def irq_handler():
    """
    Contain codes you want to execute when the interrupt is triggered. We make
    the LED flashing 20 times in this function.
    """
    # open an LEDs session
    with NIELVISIIIAcademicIO.LEDs() as LED:
        # specfy the led which to turn on and off
        led = Led.LED0
        # specify statuses
        led_on = True
        led_off = False
        # The program writes value 20 times
        for x in range(0, 20):
            # turn LED0 on
            LED.write(led, led_on)
            # delay for 0.5 seconds so that the program does not run too fast
            time.sleep(0.5)
            # turn LED0 off
            LED.write(led, led_off)
            # delay for 0.5 seconds so that the program does not run too fast
            time.sleep(0.5)

# open an ButtonIRQ session
with NIELVISIIIAcademicIO.ButtonIRQ() as Button_IRQ:
	# specify the identifier of the interrupt to register
	irq_number = IRQNumber.IRQ1
	# specify the amount of time for timeout when interrupt is not triggered
	timeout= 6000
	# specify when to register or create an interrupt based on the signal
	interrupt_type_rising = True
	interrupt_type_falling = False
	# specify the number of edges of the signal that must occur for this
    # example to register an interrup
	edge_count = 2

	# waitting for the interrupt or timeout
	Button_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)