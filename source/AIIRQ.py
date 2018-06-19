"""
NI ELVIS III Analog Input Interrupt (AI IRQ) Example
This example illustrates how to register analog input interrupts on the NI
ELVIS III. To do so, you need to first create an analog input interrupt
session, and then configure an interrupt.

To create an analog input interrupt session, you need to define irq_channel,
which is a required parameter. Since the NI ELVIS III only provides two analog
input interrupt channels, AI0 and AI1 on bank A, irq_channel must be either
AIIRQChannel.AI0 or AIIRQChannel.AI1.

To configure an interrupt, you need to define six parameters: irq_handler,
irq_number, timeout, threshold, hysteresis, and irq_type. irq_handler is a
required parameter. It defines the callback function which you use to handle
interrupts. The callback function executes when the interrupt occurs. You can
customize the callback function as needed. For example, you can write code to
make an LED flash as shown in this example, or to read from an AI channel. All
the other five parameters are optional. The default values of the optional
parameters are:
    irq_number: IRQ1
    timeout: 10000
    threshold: 2.5
    hysteresis: 0.02
    irq_type: RISING

Note: irq_number specifies the identifier of the interrupt to register.
The valid values are from IRQ1 to IRQ7. You cannot register an I/O interrupt
with the same IRQ number as that of a registered I/O interrupt. However, after
you close the existing interrupt, you can use the IRQ number to register
another interrupt.

Hardware setup:
    Connect an analog signal source to AI0 on bank A.

Result:
    An interrupt occurs when AI0 receives an appropriate analog signal.
    The program calls irq_handler when the interrupt occurs.
"""
import time
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
    threshold = 4.0
    # specify a window, in volts, above or below threshold. This program uses
    # hysteresis to prevent false interrupt registration
    hysteresis = 0.02
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