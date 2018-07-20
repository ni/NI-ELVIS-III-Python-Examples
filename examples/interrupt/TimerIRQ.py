"""
NI ELVIS III Timer Interrupt Example
This example illustrates how to register a timer interrupt (TimerIRQ) on the
NI ELVIS III. The program first defines the configuration for the Timer IRQ,
then waits for a specific time. When the time is arrived, the irq_handler
function will be called.

irq_handler is a required parameter. It defines the callback function which
you use to handle interrupts. The callback function executes when the
interrupt occurs. You can customize the callback function as needed. For
example, you can write code to make an LED flash as shown in this example, or
to read from an AI channel.

Hardware setup:
    No hardware is needed.

Result:
    An interrupt occurs when the time interval is reached.
    The program calls irq_handler when the interrupt occurs.
"""
import time
import sys
sys.path.append('source/nielvisiii')
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

# open a timer interrupt session
with academicIO.TimerIRQ() as Timer_IRQ:
        # specify the span of time, in milliseconds, between when the program
        # starts and when an interrupt occurs
        irq_interval= 5000000    # 5000000us = 5s

        # wait for the interrupt or timeout
        Timer_IRQ.configure(irq_handler, irq_interval)