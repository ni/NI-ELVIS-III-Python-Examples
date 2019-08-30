"""
Output:
    The interrupt event occurs based on the time interval; otherwise timeout.
    The irq_handler function is called when the interrupt occured.
"""
import unittest

from nielvis import TimerIRQ

def irq_handler():
    print("Timer interrupt is triggered. Now it is callback time.")

class Test_TimerIRQ(unittest.TestCase):
    def test_WaitFor5s_DoesnotShowError(self):
        irq_interval= 5000000    # 5s
        with TimerIRQ(irq_handler, irq_interval) as Timer_IRQ:
            Timer_IRQ.wait()
