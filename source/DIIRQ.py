"""
NI ELVIS III Digital Input Interrupt (DIIRQ) Example
This example illustrates how to register digital input interrupts on the NI
ELVIS III. To do so, you need to first create a digital input interrupt
session, and then configure an interrupt.

To create an digital input interrupt session, you need to define irq_channel,
which is a required parameter. Since the NI ELVIS III only provides four digital
input interrupt channels, DIO0 to DIO3 on bank A, irq_channel must be bwtween
DIIRQChannel.DIO0 to DIIRQChannel.DIO3.

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
    Connect a digital signal source to DIO0 on bank A.

Result:
    An interrupt occurs when DIO0 receives an appropriate digital signal.
    The program calls irq_handler when the interrupt occurs.
"""
import time
import academicIO
from enums import DIOChannel, IRQNumber, Led

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

# specify the DIO channel that serves as the interrupt channel
irq_channel = DIOChannel.DIO0
# open a digital input interrupt session, and set the initial values for the
# parameters
with academicIO.DIIRQ(irq_channel) as DI_IRQ:
	# specify the identifier of the interrupt to register
	irq_number = IRQNumber.IRQ1
	# specify the amount of time, in milliseconds, to wait for an interrupt to
	# occur before timing out
	timeout= 6000
	# specify whether to register an interrupt on the rising edge or the
    # falling edge of the digital input signal. To register an interrupt on
    # the rising edge of the digital input signal, set interrupt_type_rising
    # as True and interrupt_type_falling as False
	interrupt_type_rising = True
	interrupt_type_falling = False
	# specify the number of edges of the signal that must occur for this
    # program to register an interrupt. For example, when
    # interrupt_type_rising is True and edge_count is 1, an interrupt occurs
    # when the DIO channel receives one appropriate rising edge
	edge_count = 1

	# wait for the interrupt or timeout
	DI_IRQ.configure(irq_handler,
					 irq_number,
					 timeout,
					 interrupt_type_rising,
					 interrupt_type_falling,
					 edge_count)