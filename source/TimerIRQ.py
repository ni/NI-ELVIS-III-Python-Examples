"""
NI ELVIS III Timer Interrupt (TimerIRQ) Example
This example illustrates how to trigger an TimerIRQ on NI ELVIS III.To
configure and wait on an interrupt triggered, you need to define two
parameters: irq_interval and timeout. IRQ interval is a required parameter.
The other parameters are optional. The default values of the optional
parameters are:
    timeout: 10000

Output:
    The interrupt event occurs when the time interval is reached.
    The irq_handler function is called when the interrupt is triggered.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import Led

def irq_handler():
    """
    Contain codes you want to execute when the interrupt is triggered. We make
    the LED flashing in this function.
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
            # delay for 2 seconds so that the program does not run too fast
            time.sleep(1)
            # turn LED0 off
            LED.write(led, led_off)
            # delay for 2 seconds so that the program does not run too fast
            time.sleep(1)

# open an TimerIRQ session
with NIELVISIIIAcademicIO.TimerIRQ() as Timer_IRQ:
        # specify the span of time between interrupts in microseconds
        irq_interval= 5000000    # 5000000us = 5s

        # waitting for the interrupt or timeout
        Timer_IRQ.configure(irq_handler, irq_interval)