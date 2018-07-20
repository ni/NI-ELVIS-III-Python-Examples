"""
NI ELVIS III Timer Interrupt Example
This example illustrates how to register a timer interrupt (TimerIRQ) on the
NI ELVIS III. The program first defines the configuration for the Timer IRQ,
then waits for a specific time. When the time is arrived, the irq_handler
function will be called.

The Timer IRQ configuration consists of two parameters: irq_handler and
irq_interval. irq_handler defines the callback function which you use to
handle interrupts. The callback function executes when the interrupt occurs.
You can customize the callback function as needed. For example, you can write
code to make an LED flash as shown in this example, or to read from an AI
channel.

Hardware setup:
    No hardware is needed.

Result:
    The LED0 flashes for 25 seconds. An interrupt occurs when the interrupt
    condition, time interval is reached. The program calls irq_handler, which
    makes the LED1 flashes for 3 seconds, when the interrupt occurs.
"""
import time
import thread
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

# specify the span of time, in milliseconds, between when the program
# starts and when an interrupt occurs
irq_interval= 5000000    # 5000000us = 5s
# open a timer interrupt session
with academicIO.TimerIRQ(irq_handler, irq_interval) as Timer_IRQ:
    # open the LED session
    LED = academicIO.LEDs()
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True

    # create a thread for interrupt
    thread.start_new_thread(Timer_IRQ.wait, ())

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
