"""
NI ELVIS III Analog Input Interrupt Example
This example illustrates how to register analog input interrupts (AI IRQ) on
the NI ELVIS III. The program first defines the configuration for the AI
channel, then waits for an appropriate analog signal. When the AI channel
receive the signal, the irq_handler function will be called.

The AI IRQ configuration consists of one parameter: irq_channel. There is one
identical bank of AI IRQ channels: A. Bank A contains 2 analog input
interrupt channels (AI0 and AI1).

To executes the configure function, you need to define six parameters:
irq_handler, irq_number, timeout, threshold (0 to 5), hysteresis (0 to 1), and
irq_type (Rising and Falling).

irq_handler is a required parameter. It defines the callback function which
you use to handle interrupts. The callback function executes when the
interrupt occurs. You can customize the callback function as needed. For
example, you can write code to make an LED flash as shown in this example, or
to read from an AI channel.

irq_number specifies the identifier of the interrupt to register. There are
seven identical numbers of IRQ number (IRQ1 to IRQ8). You cannot register an
I/O interrupt with the same IRQ number as that of a registered I/O interrupt.
However, after you close the existing interrupt, you can use the IRQ number to
register another interrupt.

This example uses:
    Bank A, Channel AI0.

This example uses:
    Bank A, Channel AI0.

Hardware setup:
    Connect an analog signal source to AI0 on bank A. Gives an appropriate
    analog signal before the program ends. You can connect BTN0 to AI0 on
    bank A to trigger the interrupt as indicated in this table:
        1. Connect BTN0 A to AI0 on bank A, then connect to a 10k Ohm
           resistance.
        2. Connect a +3.3 V voltage source to the 10k Ohm resistance.
        3. Connect BTN0 B to DGND.
    Then, press the button BTN0.

Result:
    An interrupt occurs when AI0 receives an appropriate analog signal.
    The program calls irq_handler when the interrupt occurs.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import AIIRQChannel, IRQNumber, AIIRQType, Led

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

# specify the AI channel that serves as the interrupt channel
irq_channel = AIIRQChannel.AI0
# open an analog input interrupt session, and set the initial values for the
# parameters
with academicIO.AIIRQ(irq_channel) as AI_IRQ:
    # specify the identifier of the interrupt to register
    irq_number = IRQNumber.IRQ1
    # specify the amount of time, in milliseconds, to wait for an interrupt to
    # occur before timing out
    timeout = 6000
    # specify the value, in volts, that the signal must cross for this example
    threshold = 1
    # specify a window, in volts, above or below threshold. This program uses
    # hysteresis to prevent false interrupt registration
    hysteresis = 0.05
    # specify whether to register an interrupt on the falling edge or rising
    # edge of the analog input signal
    irq_type = AIIRQType.RISING

    # wait for the interrupt or timeout
    AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     threshold,
                     hysteresis,
                     irq_type)
