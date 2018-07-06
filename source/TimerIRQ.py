"""
NI ELVIS III Timer Interrupt (TimerIRQ) Example
This example illustrates how to register a timer interrupt on the NI ELVIS
III. To do so, you need to first create a timer interrupt session, and then
configure an interrupt.

To configure an interrupt, you need to define two parameters: irq_handler,
and irq_interval. Both irq_handler and irq_interval are required parameters. 
irq_handler defines the callback function which you use to handle interrupts.
The callback function executes when the interrupt occurs. You can customize
the callback function as needed. For example, you can write code to make an
LED flash as shown in this example, or to read from an AI channel.

Hardware setup:
    No hardware is needed.

Result:
    An interrupt occurs when the time interval is reached.
    The program calls irq_handler when the interrupt occurs.
"""
import time
import academicIO
from enums import Led

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

# open a timer interrupt session
with academicIO.TimerIRQ() as Timer_IRQ:
        # specify the span of time, in milliseconds, between when the program
        # starts and when an interrupt occurs
        irq_interval= 5000000    # 5000000us = 5s

        # wait for the interrupt or timeout
        Timer_IRQ.configure(irq_handler, irq_interval)