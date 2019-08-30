"""
Output:
    The interrupt event occurs when a digital signal is inputed.
    The callback_function is called when the interrupt occured.
"""
import unittest
from nielvis import DIIRQ, DIIRQChannel, IRQNumber

def irq_handler():
    print("DI interrupt is triggered. Now it is callback time.")

class Test_DIIRQ(unittest.TestCase):
    def test_OpenWithDifferentArgs_ShowExpectedResult(self):
        testcases = [
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': 1},
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': True, 'edge_count': 1},
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': True, 'edge_count': 1},
        ]

        for testcase in testcases:
            with DIIRQ(testcase['irq_channel'],
                                irq_handler,
                                testcase['irq_number'],
                                testcase['timeout'],
                                testcase['interrupt_type_rising'],
                                testcase['interrupt_type_falling'],
                                testcase['edge_count']) as DI_IRQ:
                DI_IRQ.wait()

class Test_DIIRQ_OpenAssertion(unittest.TestCase):
    def __open_with_assertion(self, testcase):
        with self.assertRaises(AssertionError):
                DI_IRQ = DIIRQ(testcase['irq_channel'],
                               irq_handler,
                               testcase['irq_number'],
                               testcase['timeout'],
                               testcase['interrupt_type_rising'],
                               testcase['interrupt_type_falling'],
                               testcase['edge_count'])

    def test_OpenWithInvalidInterruptType_ShowAssertion(self):
        testcases = [
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': 1},
        ]

        for testcase in testcases:
            self.__open_with_assertion(testcase)

    def test_OpenWithInvalidIrqNumber_ShowAssertion(self):
        invalid_irq_number = 0
        testcases = [
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': invalid_irq_number, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': 1},
        ]

        for testcase in testcases:
            self.__open_with_assertion(testcase)

    def test_OpenWithInvalidTimeout_ShowAssertion(self):
        invalid_timeout = -1
        testcases = [
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': invalid_timeout, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': 1},
        ]

        for testcase in testcases:
            self.__open_with_assertion(testcase)

    def test_OpenWithInvalidEdgeCount_ShowAssertion(self):
        invalid_edge_count = [0, 4294967296]
        testcases = [
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': invalid_edge_count[0]},
            {'irq_channel': DIIRQChannel.DIO1, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': invalid_edge_count[1]},
        ]

        for testcase in testcases:
            self.__open_with_assertion(testcase)

    def test_OpenWithInvalidIrqChannel_ShowAssertion(self):
        invalid_irq_channel = 4
        testcases = [
            {'irq_channel': invalid_irq_channel, 'irq_number': IRQNumber.IRQ2, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': 1},
        ]

        for testcase in testcases:
            self.__open_with_assertion(testcase)
