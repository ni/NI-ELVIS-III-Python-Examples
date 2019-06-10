"""
NI ELVIS III Timer Interrupt Example
This example illustrates how to register a timer interrupt (Timer IRQ) on the
NI ELVIS III. The program first defines the configuration for the Timer IRQ,
and then creates a thread to wait for an interrupt. The irq_handler function
executes when the interval is reached.

The Timer IRQ configuration consists of two parameters: irq_handler and
irq_interval. irq_handler defines the callback function which you use to
handle interrupts. The callback function executes when the interrupt occurs.
You can customize the callback function as needed. For example, you can write
code to make an LED flash as shown in this example, or to read from an AI
channel.

This example uses:
    NI ELVIS III FPGA timer.

Hardware setup:
    No hardware is needed.

Result:
    A thread is created to wait for an interrupt. LED0 flashes for 25 seconds
    while waiting for an interrupt. An interrupt occurs when the interval is
    reached. The program then calls the irq_handler function, which makes LED1
    flash for 3 seconds. While LED1 is flashing, LED0 will also keep flashing
    until the program ends.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import thread
import academicIO
from enums import Led

def irq_handler():
    """
    irq_handler contains the code you want to execute when the interrupt
    occurs. Define your own callback function here by rewriting the code. We
    make an LED flash in this example.
    """
    # open an LED session
    with academicIO.LEDs() as LED:
        # specify the LED which you want to control
        led = Led.LED1
        # specify the LED status
        led_on_off = True
        # writes values 10 times, which makes LED1 flash for 3 seconds
        for x in range(0, 10):
            # turn LED0 on or off
            LED.write(led, led_on_off)
            # add a short delay
            time.sleep(0.3)
            # if the LED is on, set the parameter to off
            # if the LED is off, set the parameter to on
            led_on_off = not led_on_off

# specify the span of time, in milliseconds, between when the program
# starts and when an interrupt occurs
irq_interval= 5000000    # 5000000us = 5s
# configure a timer interrupt session
with academicIO.TimerIRQ(irq_handler, irq_interval) as Timer_IRQ:
    # open the LED session
    LED = academicIO.LEDs()
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True

    # create a thread to wait for the interrupt
    thread.start_new_thread(Timer_IRQ.wait, ())

    # writes values 50 times, which makes LED0 flash for 25 seconds
    for x in range(0, 50):
        # turn LED0 on or off
        LED.write(led, led_on_off)
        # add a short delay
        time.sleep(0.5)
        # if the LED is on, set the parameter to off
        # if the LED is off, set the parameter to on
        led_on_off = not led_on_off
    
    # close the LED session
    LED.close()
