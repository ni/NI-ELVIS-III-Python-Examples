"""
NI ELVIS III Button Interrupt Example
This example illustrates how to register button interrupts (ButtonIRQ) on the
NI ELVIS III. The program first defines the configuration for the Button IRQ,
then waits for BUTTON 0 to be pressed. When the button is pressed, the
irq_handler function will be called.

The Button IRQ configuration consists of six parameters: irq_handler, irq_number,
timeout, interrupt_type_rising, interrupt_type_falling, and edge_count.

irq_handler defines the callback function which you use to handle interrupts.
The callback function executes when the interrupt occurs. You can customize
the callback function as needed. For example, you can write code to make an
LED flash as shown in this example, or to read from an AI channel.

irq_number specifies the identifier of the interrupt to register. There are
8 IRQ numbers (IRQ1 to IRQ8). You cannot register an I/O interrupt with the
same IRQ number as that of a registered I/O interrupt. However, after you
close the existing interrupt, you can use the IRQ number to register another
interrupt.

This example uses:
    User programmable button BUTTON 0.

Hardware setup:
    Press the button BUTTON 0 on NI ELVIS III before the program ends.

Result:
    The LED0 flashes for 25 seconds. An interrupt occurs when the button
    BUTTON 0 is pressed. Press the button to trigger the interrupt within 25
    seconds. The program calls irq_handler, which makes the LED1 flashes for 3
    seconds, when the interrupt occurs.
"""
import time
import thread
import sys
sys.path.append('source/nielvisiii')
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

# specify the identifier of the interrupt to register
irq_number = IRQNumber.IRQ1
# specify the amount of time, in milliseconds , to wait for an interrupt
# to occur before timing out
timeout = 6000
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
# open a button interrupt session
with academicIO.ButtonIRQ(irq_handler,
                          irq_number,
                          timeout,
                          interrupt_type_rising,
                          interrupt_type_falling,
                          edge_count) as Button_IRQ:
    # open the LED session
    LED = academicIO.LEDs()
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True

    # create a thread for interrupt
    thread.start_new_thread(Button_IRQ.wait, ())

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
