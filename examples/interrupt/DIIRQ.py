"""
NI ELVIS III Digital Input Interrupt Example
This example illustrates how to register a digital input interrupt (DI IRQ) on
the NI ELVIS III. The program first defines the configuration for the DI IRQ,
then creates a thread to wait for an interrupt. The irq_handler function
executes when the DI channel receives an appropriate digital signal to trigger
the interrupt conditions.

The DI IRQ configuration consists of seven parameters: irq_channel, irq_handler,
irq_number, timeout, interrupt_type_rising, interrupt_type_falling, and
edge_count. There are four DI channels support DI IRQ configuration, which are
DIO0 to DIO3 on bank A. Each configuration contains two parmeters to define
whether to register the interrupt at the rising edge or falling edge as
indicated in this table:
    interrupt_type_rising    True    False   True
    interrupt_type_falling   False   True    True
There are 8 IRQ numbers (IRQ1 to IRQ8). You cannot register an I/O interrupt
with the same IRQ number as that of a registered I/O interrupt. However, after
you close the existing interrupt, you can use the IRQ number to register another
interrupt.
 
irq_handler defines the callback function which you use to handle interrupts.
The callback function executes when the interrupt occurs. You can customize
the callback function as needed. For example, you can write code to make an
LED flash as shown in this example, or to read from an AI channel.

This example uses:
    Bank A, Channel DIO0.

Hardware setup:
    Connect a digital signal source to DIO0 on bank A. Gives a digital signal
    to match the interrupt conditions we set in the configuration before the
    timeout expires. You can connect BTN0 to DIO0 on bank A to trigger the
    interrupt as indicated in this table:
        1. Connect BTN0 A to DIO0 on bank A, then connect to a 10k Ohm
           resistance.
        2. Connect a +3.3 V voltage source to the 10k Ohm resistance.
        3. Connect BTN0 B to DGND.
    Then, press the button BTN0. The interrupt is triggered when you press the
    button.

Result:
    The LED0 flashes for 25 seconds. An interrupt occurs when DIO0 receives an
    appropriate digital signal and the signal triggers the interrupt conditions.
    Press the button BTN0 to trigger the interrupt before the timeout expires.
    The program then calls the irq_handler function, which makes the LED1
    flashes for 3 seconds.
"""
import time
import thread
import sys
sys.path.append('source/nielvisiii')
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
        led = Led.LED1
        # specify the LED status
        led_on_off = True
        # writes values 10 times which turns LED1 on/off 5 times
        for x in range(0, 10):
            # turn LED0 on/off
            LED.write(led, led_on_off)
            # add a short delay
            time.sleep(0.3)
            # if the led is on, set the paramter to off
            # if the led is off, set the paramter to on
            led_on_off = not led_on_off

# specify the DIO channel that serves as the interrupt channel
irq_channel = DIOChannel.DIO0
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
# configure a digital input interrupt session
with academicIO.DIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      interrupt_type_rising,
                      interrupt_type_falling,
                      edge_count) as DI_IRQ:
    # open the LED session
    LED = academicIO.LEDs()
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True

    # create a thread to wait for the interrupt
    thread.start_new_thread(DI_IRQ.wait, ())

    # writes values 50 times which turns LED0 on/off 25 times
    for x in range(0, 50):
        # turn LED0 on/off
        LED.write(led, led_on_off)
        # add a short delay
        time.sleep(0.5)
        # if the led is on, set the paramter to off
        # if the led is off, set the paramter to on
        led_on_off = not led_on_off
    
    # close the LED session
    LED.close()
