"""
Hardware setup:
    1. Connect AO0 and AI0 on connector A.

Output:
    The interrupt event occurs when a analog signal is inputed.
    The irq_handler funciton is called when the interrupt occured.
"""
import time
import unittest
import threading

from nielvis import AIIRQ, AIIRQChannel, IRQNumber, AIIRQType, AnalogOutput, AOChannel, Bank

irq_channel = AIIRQChannel.AI1
irq_number = IRQNumber.IRQ3
timeout = 5000
threshold = 2.0
hysteresis = 0.5
irq_type = AIIRQType.RISING

class Test_AIIRQ(unittest.TestCase):
    def setUp(self):
        self.AO = AnalogOutput({'bank': Bank.A, 'channel': AOChannel.AO0})
        self.success = False

    def tearDown(self):
        self.AO.close()

    @classmethod
    def setUpClass(self):
        self.rising_array = [0,1,2,3,4]
        self.falling_array = [4,3,2,1,0]

    def __irq_handler(self):
        self.success = True

    def __reading_thread(self, value_to_write):
        # wait for the irq to be ready
        time.sleep(0.7)
        self.AO.write(value_to_write, 1000)

    def test_OpenWithRisingEdgeAndWaitForInterrupt_IrqNumberWasAsserted(self):
        irq_type = AIIRQType.RISING

        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.rising_array,))
        
        with AIIRQ(AIIRQChannel.AI0,
                   self.__irq_handler,
                   irq_number,
                   timeout,
                   threshold,
                   hysteresis,
                   irq_type) as AI_IRQ:

            irq_thread.start()

            AI_IRQ.wait()

        irq_thread.join()

        self.assertTrue(self.success)

    def test_OpenWithRisingEdgeAndWaitForInterrupt_IrqNumberWasNotAsserted(self):
        irq_type = AIIRQType.RISING

        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.falling_array,))
        
        with AIIRQ(AIIRQChannel.AI0,
                   self.__irq_handler,
                   irq_number,
                   timeout,
                   threshold,
                   hysteresis,
                   irq_type) as AI_IRQ:

            irq_thread.start()

            AI_IRQ.wait()

        irq_thread.join()

        self.assertFalse(self.success)

    def test_OpenWithFallingEdgeAndWaitForInterrupt_IrqNumberWasAsserted(self):
        irq_type = AIIRQType.FALLING

        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.falling_array,))
        
        with AIIRQ(AIIRQChannel.AI0,
                   self.__irq_handler,
                   irq_number,
                   timeout,
                   threshold,
                   hysteresis,
                   irq_type) as AI_IRQ:

            irq_thread.start()

            AI_IRQ.wait()

        irq_thread.join()

        self.assertTrue(self.success)

    def test_OpenWithFallingEdgeAndWaitForInterrupt_IrqNumberWasNotAsserted(self):
        irq_type = AIIRQType.FALLING

        irq_thread = threading.Thread(target=self.__reading_thread, args=(self.rising_array,))
        
        with AIIRQ(AIIRQChannel.AI0,
                   self.__irq_handler,
                   irq_number,
                   timeout,
                   threshold,
                   hysteresis,
                   irq_type) as AI_IRQ:

            irq_thread.start()

            AI_IRQ.wait()

        irq_thread.join()

        self.assertFalse(self.success)

class Test_AIIRQ_OpenAssertion(unittest.TestCase):
    def irq_handler():
        print("AI interrupt is triggered. Now it is callback time.")

    def test_OpenWithInvalidIrqNumber_ShowAssertion(self):
        invalid_irq_numbers = [0, '', []]

        for invalid_irq_number in invalid_irq_numbers:
            with self.assertRaises(AssertionError):
                AIIRQ(irq_channel,
                    self.irq_handler,
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
                      self.irq_handler,
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
                      self.irq_handler,
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
                      self.irq_handler,
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
                      self.irq_handler,
                      irq_number,
                      timeout,
                      threshold,
                      hysteresis,
                      invalid_irq_type)
