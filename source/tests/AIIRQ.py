"""
Output:
    The interrupt event occurs when a analog signal is inputed.
    The irq_handler funciton is called when the interrupt occured.
"""
import time
import academicIO
from enums import *

def irq_handler():
    print "AI interrupt is triggered. Now it is callback time."

irq_channel = AIIRQChannel.AI1
with academicIO.AIIRQ(irq_channel) as AI_IRQ:
    irq_number = IRQNumber.IRQ3
    timeout = 6000
    threshold = 4.0
    hysteresis = 0.02
    irq_type = AIIRQType.RISING
    AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     threshold,
                     hysteresis,
                     irq_type)

    irq_type = AIIRQType.FALLING
    AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     threshold,
                     hysteresis,
                     irq_type)

    try:
		AI_IRQ.configure(irq_handler,
                     0,
                     timeout,
                     threshold,
                     hysteresis,
                     irq_type)
    except AssertionError:
		print "Caught the error - 0 can't be irq_number of AIIRQ."

    try:
		AI_IRQ.configure(irq_handler,
                     irq_number,
                     -1,
                     threshold,
                     hysteresis,
                     irq_type)
    except AssertionError:
		print "Caught the error - the timeout value should be greater than 0."

    try:
		AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     6,
                     hysteresis,
                     irq_type)
    except AssertionError:
		print "Caught the error - the threshold value should be [0-5]."

    try:
		AI_IRQ.configure(irq_handler,
                     irq_number,
                     timeout,
                     threshold,
                     1.2,
                     irq_type)
    except AssertionError:
		print "Caught the error - the hysteresis value should be [0-1]."

irq_channel = 2
try:
	academicIO.AIIRQ(irq_channel)
except AssertionError:
	print "Caught the error - The channels available in the AIIRQ should be 0-1."