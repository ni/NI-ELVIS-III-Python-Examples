"""
NI ELVIS III Analog Input Interrupt (AIIRQ) Example
This example illustrates how to trigger an AIIRQ on NI ELVIS III. To create an
AIIRQ session, you need to define a required parameter: irq_channel. Since NI
ELVIS III only provides four Digital Input Interrupt channels: AI0 and AI1 on
bank A, irq_channel has to be within the range [0:1]. To configure and wait on
an interrupt triggered, you need to define six parameters: irq_handler,
irq_number, timeout, threshold, hysteresis, and irq_type. You must use
callback function to handle interrupt. The callback function contains code
that handles interrupts and runs when the interrupts triggering occurs. The
other parameters are optional. The default values of the optional parameters
are:
    irq_number: 3
    timeout: 10000
    threshold: 2.5
    hysteresis: 0.02
    irq_type: 'rising'

Note: irq_number refers to the irq number of this interrupt event. The valid
values are within the range [1:7]. You cannot register an I/O interrupt with
the same IRQ number as a registered I/O interrupt. However, after you closed
the existing interrupt, you can use the IRQ number to register another
interrupt.

Hardware setup:
    1. Connect an analog signal source to AI0 on bank A.

Output:
    The interrupt event occurs when an appropriately analog signal is given.
    The irq_handler function is called when the interrupt is triggered.
"""
import time
import NIELVISIIIAcademicIO
from NIELVISIIIEnum import AIIRQChannel, IRQNumber, AIIRQType, Led

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

# specify the AI channel to register and create the AIIRQ
irq_channel = AIIRQChannel.AI0
# open an AIIRQ session, and set the initial values for the parameters
with NIELVISIIIAcademicIO.AIIRQ(irq_channel) as AI_IRQ:
    # specify the identifier of the interrupt to register
    irq_number = IRQNumber.IRQ1
    # specify the amount of time for timeout when interrupt is not triggered
    timeout = 6000
    # specify the value, in volts, that the signal must cross for this example
    # to register an interrupt
    threshold = 4.0
    # specify the value that used to avoid false triggering due to noise or
    # jitter in the signal
    hysteresis = 0.02
    # specify when to register or create an interrupt based on the signal
    irq_type = AIIRQType.RISING

    # waitting for the interrupt or timeout
    AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     threshold,
                     hysteresis,
                     irq_type)