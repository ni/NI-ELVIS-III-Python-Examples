"""
NI ELVIS III Analog Input Interrupt Example
This example illustrates how to register an analog input interrupt (AI IRQ) on
the NI ELVIS III. The program first defines the configuration for the AI IRQ,
and then creates a thread to wait for an interrupt. The irq_handler function
executes when the AI channel receives an appropriate analog signal to trigger
the interrupt conditions.

The AI IRQ configuration consists of seven parameters: irq_channel,
irq_handler, irq_number, timeout, threshold, hysteresis, and irq_type. There
are two AI channels that support AI IRQ configuration, which are AI0 and AI1 on
bank A. The AI IRQ contains two types of edge (rising and falling) with a
threshold from 0 to 5 and hysteresis from 0 to 1. There are 8 IRQ numbers
(IRQ1 to IRQ8). You cannot register an I/O interrupt with the same IRQ number
as that of a registered I/O interrupt. However, after you close the existing
interrupt, you can use the IRQ number to register another interrupt.

irq_handler defines the callback function which you use to handle interrupts.
The callback function executes when the interrupt occurs. You can customize
the callback function as needed. For example, you can write code to make an
LED flash as shown in this example, or to read from an AI channel.

This example uses:
    Bank A, Channel AI0.

Hardware setup:
    Connect an analog signal source to AI0 on bank A. Send an analog signal
    that meets the interrupt conditions we configure before the timeout
    expires. You can connect BTN0 to AI0 on bank A to trigger the interrupt as
    indicated in this table:
        1. Connect a pin of a 10k Ohm resistance to both BTN0 A and AI0 on
           bank A.
        2. Connect a +3.3 V voltage source to another pin of the 10k Ohm
           resistance.
        3. Connect BTN0 B to DGND.
    Press BTN0. The interrupt is triggered.

Result:
    A thread is created to wait for an interrupt. LED0 flashes for 25 seconds
    while waiting for an interrupt. An interrupt occurs when AI0 receives an
    appropriate analog signal that meets the interrupt conditions. To trigger
    the interrupt, press BTN0 before the timeout expires. The program then
    calls the irq_handler function, which makes LED1 flash for 3 seconds.
    While LED1 is flashing, LED0 will also keep flashing until the program
    ends.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'source/nielvisiii'))

import time
import threading
import academicIO
from enums import AIIRQChannel, IRQNumber, AIIRQType, Led

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
        # write values 10 times, which makes LED1 flash for 3 seconds
        for x in range(0, 10):
            # turn LED1 on or off
            LED.write(led, led_on_off)
            # add a short delay
            time.sleep(0.3)
            # if the LED is on, set the parameter to off
            # if the LED is off, set the parameter to on
            led_on_off = not led_on_off

# specify the AI channel that serves as the interrupt channel
irq_channel = AIIRQChannel.AI0
# specify the identifier of the interrupt to register
irq_number = IRQNumber.IRQ1
# specify the amount of time, in milliseconds, to wait for an interrupt to
# occur before timing out
timeout = 6000
# specify the value, in volts, that the signal must cross for the interrupt to
# occur
threshold = 1
# specify a window, in volts, above or below threshold. This program uses
# hysteresis to prevent false interrupt registration
hysteresis = 0.05
# specify whether to register an interrupt on the falling edge or rising
# edge of the analog input signal
irq_type = AIIRQType.RISING
# configure an analog input interrupt session
with academicIO.AIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      threshold,
                      hysteresis,
                      irq_type) as AI_IRQ:
    # open the LED session
    LED = academicIO.LEDs()
    # specify the LED which you want to control
    led = Led.LED0
    # specify the LED status
    led_on_off = True

    # create a thread to wait for the interrupt
    irq_thread = threading.Thread(target=AI_IRQ.wait)
    irq_thread.start()

    # write values 50 times, which makes LED0 flash for 25 seconds
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
