"""
NI ELVIS III Digital Input Interrupt Example
This example illustrates how to register digital input interrupts (DIIRQ) on
the NI ELVIS III. The program first defines the configuration for the DI IRQ,
then waits for an appropriate digital signal. When the DI channel receive the
signal, the irq_handler function will be called.

The DI IRQ configuration consists of one parameter: irq_channel. There is one
identical bank of DI IRQ channels: A. Bank A contains 4 digital input
interrupt channels (DIO0 to DIO3).

The configure function consists six parameters: irq_handler, irq_number,
timeout, interrupt_type_rising, interrupt_type_falling, and edge_count.

irq_handler is a required parameter. It defines the callback function which
you use to handle interrupts. The callback function executes when the
interrupt occurs. You can customize the callback function as needed. For
example, you can write code to make an LED flash as shown in this example, or
to read from an AI channel.

irq_number specifies the identifier of the interrupt to register. There are
seven identical numbers of IRQ number (IRQ1 to IRQ7). You cannot register an
I/O interrupt with the same IRQ number as that of a registered I/O interrupt.
However, after you close the existing interrupt, you can use the IRQ number to
register another interrupt.

This example uses:
    Bank A, Channel DIO0.

Hardware setup:
    Connect a digital signal source to DIO0 on bank A. Gives an appropriate
    digital signal before the program ends. You can connect BTN0 to DIO0 on
    bank A to trigger the interrupt as indicated in this table:
        1. Connect BTN0 A to DIO0 on bank A, then connect to a 10k Ohm
           resistance.
        2. Connect a +3.3 V voltage source to the 10k Ohm resistance.
        3. Connect BTN0 B to DGND.
    Then, press the button BTN0.

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
        # writes values 5 times
        for x in range(0, 5):
            # turn LED0 on
            LED.write(led, led_on)
            # add a short delay before acquiring next data point
            time.sleep(1)
            # turn LED0 off
            LED.write(led, led_off)
            # add a short delay before acquiring next data point
            time.sleep(1)

# specify the DIO channel that serves as the interrupt channel
irq_channel = DIOChannel.DIO0
# open a digital input interrupt session
with academicIO.DIIRQ(irq_channel) as DI_IRQ:
    # specify the identifier of the interrupt to register
    irq_number = IRQNumber.IRQ1
    # specify the amount of time, in milliseconds, to wait for an interrupt to
    # occur before timing out
    timeout = 6000
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
