"""
Output:
    The interrupt event occurs based on the time interval; otherwise timeout.
    The irq_handler function is called when the interrupt occured.
"""
import time
import academicIO
from enums import *

def irq_handler():
    print "Timer interrupt is triggered. Now it is callback time."

with academicIO.TimerIRQ() as Timer_IRQ:
    irq_interval= 5000000    # 5s

    Timer_IRQ.configure(irq_handler, irq_interval)