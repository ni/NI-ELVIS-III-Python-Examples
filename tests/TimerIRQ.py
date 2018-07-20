"""
Output:
    The interrupt event occurs based on the time interval; otherwise timeout.
    The irq_handler function is called when the interrupt occured.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

def irq_handler():
    print "Timer interrupt is triggered. Now it is callback time."

irq_interval= 5000000    # 5s
with academicIO.TimerIRQ(irq_handler, irq_interval) as Timer_IRQ:
    Timer_IRQ.wait()
