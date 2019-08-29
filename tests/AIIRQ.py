"""
Output:
    The interrupt event occurs when a analog signal is inputed.
    The irq_handler funciton is called when the interrupt occured.
"""
import unittest
from nielvis import AIIRQ, AIIRQChannel, IRQNumber, AIIRQType

def irq_handler():
    print("AI interrupt is triggered. Now it is callback time.")

irq_channel = AIIRQChannel.AI1
irq_number = IRQNumber.IRQ3
timeout = 6000
threshold = 1.0
hysteresis = 0.5
irq_type = AIIRQType.RISING

class Test_AIIRQ(unittest.TestCase):
    def test_OpenWithRisingEdge_DoesnotShowError(self):
        irq_type = AIIRQType.RISING

        with AIIRQ(irq_channel,
                irq_handler,
                irq_number,
                timeout,
                threshold,
                hysteresis,
                irq_type) as AI_IRQ:
            AI_IRQ.wait()

    def test_OpenWithFallingEdge_DoesnotShowError(self):
        irq_type = AIIRQType.FALLING

        with AIIRQ(irq_channel,
                irq_handler,
                irq_number,
                timeout,
                threshold,
                hysteresis,
                irq_type) as AI_IRQ:
            AI_IRQ.wait()

class Test_AIIRQ_OpenAssertion(unittest.TestCase):
    def test_OpenWithInvalidIrqNumber_ShowAssertion(self):
        invalid_irq_numbers = [0, '', []]

        for invalid_irq_number in invalid_irq_numbers:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                    irq_handler,
                    invalid_irq_number,
                    timeout,
                    threshold,
                    hysteresis,
                    irq_type)

    def test_OpenWithInvalidTimeout_ShowAssertion(self):
        invalid_timeouts = [-1, '', []]

        for invalid_timeout in invalid_timeouts:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      invalid_timeout,
                      threshold,
                      hysteresis,
                      irq_type)

    def test_OpenWithInvalidThreshold_ShowAssertion(self):
        limits = {'min': 0, 'max': 5}
        invalid_thresholds = [limits['min'] - 1, limits['max'] + 1, '', []]

        for invalid_threshold in invalid_thresholds:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      invalid_threshold,
                      hysteresis,
                      irq_type)

    def test_OpenWithInvalidHysteresis_ShowAssertion(self):
        limits = {'min': 0, 'max': 1}
        invalid_hysteresises = [limits['min'] - 1, limits['max'] + 1, '', []]

        for invalid_hysteresis in invalid_hysteresises:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      threshold,
                      invalid_hysteresises,
                      irq_type)

    def test_OpenWithInvalidIrqType_ShowAssertion(self):
        limits = {'min': 0, 'max': 1}
        invalid_irq_types = [limits['min'] - 1, limits['max'] + 1, '', []]

        for invalid_irq_type in invalid_irq_types:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                      irq_handler,
                      irq_number,
                      timeout,
                      threshold,
                      hysteresis,
                      invalid_irq_type)
