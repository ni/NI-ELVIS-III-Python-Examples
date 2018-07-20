"""
NI ELVIS III Analog Input Interrupt Example
This example illustrates how to register analog input interrupts (AI IRQ) on
the NI ELVIS III. The program first defines the configuration for the AI
channel, then waits for an appropriate analog signal. When the AI channel
receive the signal, the irq_handler function will be called.

The AI IRQ configuration consists of seven parameters: irq_channel,
irq_handler, irq_number, timeout, threshold, hysteresis, and irq_type. Only 2
channels support AI IRQ configuration, which are AI0 and AI1 on bank A. The AI
IRQ contains two types of edge (rising and falling) with a threshold from 0 to
5 and hysteresis from 0 to 1.

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
    Bank A, Channel AI0.

This example uses:
    Bank A, Channel AI0.

Hardware setup:
    Connect an analog signal source to AI0 on bank A. Gives a analog signal
    to match the interrupt conditions we set in the configuration before the
    timeout expires. You can connect BTN0 to AI0 on bank A to trigger the
    interrupt as indicated in this table:
        1. Connect BTN0 A to AI0 on bank A, then connect to a 10k Ohm
           resistance.
        2. Connect a +3.3 V voltage source to the 10k Ohm resistance.
        3. Connect BTN0 B to DGND.
    Then, press the button BTN0. The interrupt is trigger when you press the
    button.

Result:
    The LED0 flashes for 25 seconds. An interrupt occurs when AI0 receives an
    appropriate analog signal and the signal trigger the interrupt conditions.
    Press the button BTN0 to trigger the interrupt within 25 seconds. The
    program calls irq_handler, which makes the LED1 flashes for 3 seconds,
    when the interrupt occurs.
"""
import time
import thread
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

# specify the AI channel that serves as the interrupt channel
irq_channel = AIIRQChannel.AI0
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
# open an analog input interrupt session
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

    # create a thread for interrupt
    thread.start_new_thread(AI_IRQ.wait, ())

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