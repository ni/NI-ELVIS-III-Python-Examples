"""
NI ELVIS III Button Interrupt (ButtonIRQ) Example
This example illustrates how to register button interrupts on the NI ELVIS III.
To do so, you need to first create a button interrupt session, and then
configure an interrupt.

To configure an interrupt, you need to define six parameters: irq_handler,
irq_number, timeout, interrupt_type_rising, interrupt_type_falling, and
edge_count. irq_handler is a required parameter. It defines the callback
function which you use to handle interrupts. The callback function executes
when the interrupt occurs. You can customize the callback function as needed.
For example, you can write code to make an LED flash as shown in this example,
or to read from an AI channel. All the other five parameters are optional. The
default values of the optional parameters are:
    irq_number: IRQ1
	timeout: 10000
	interrupt_type_rising: True
	interrupt_type_falling: False
	edge_count: 1

Note: irq_number specifies the identifier of the interrupt to register.
The valid values are from IRQ1 to IRQ7. You cannot register an I/O interrupt
with the same IRQ number as that of a registered I/O interrupt. However, after
you close the existing interrupt, you can use the IRQ number to register
another interrupt.

Hardware setup:
    No hardware is needed.

Result:
    An interrupt occurs when you press the button.
    The program calls irq_handler when the interrupt occurs.
"""
import time
import academicIO
from enums import IRQNumber, Led

def irq_handler():
    """
    irq_handler contains the code you want to execute when the interrupt
    occurs. Define your own callback function here by rewriting the code. We
    make an LED flash in thie example.
    """
    # open an LED session
    with academicIO.LEDs() as LED:
        # specify the LED which you want to control
        led = Led.LED0
        # specify the LED status
        led_on = True
        led_off = False
        # The program writes values 5 times
        for x in range(0, 5):
            # turn LED0 on
            LED.write(led, led_on)
            # delay for 2 seconds so that the program does not run too fast
            time.sleep(1)
            # turn LED0 off
            LED.write(led, led_off)
            # delay for 2 seconds so that the program does not run too fast
            time.sleep(1)
            
# open a button interrupt session
with academicIO.ButtonIRQ() as Button_IRQ:
	# specify the identifier of the interrupt to register
	irq_number = IRQNumber.IRQ1
	# specify the amount of time, in milliseconds , to wait for an interrupt
    # to occur before timing out
	timeout= 6000
	# specify whether to register an interrupt when you press or release the
    # button. To register an interrupt when you press the button, set
    # interrupt_type_rising as True and interrupt_type_falling as False
	interrupt_type_rising = True
	interrupt_type_falling = False
	# specify the number of edges of the signal that must occur for this
    # program to register an interrupt. For example, when
    # interrupt_type_rising is True and edge_count is 2, an interrupt occurs
    # when you press the button twice
	edge_count = 2

	# wait for the interrupt or timeout
	Button_IRQ.configure(irq_handler,
						 irq_number,
						 timeout,
						 interrupt_type_rising,
						 interrupt_type_falling,
						 edge_count)