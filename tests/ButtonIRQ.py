"""
Output:
    The interrupt event occurs when the button is clicked; otherwise timeout.
    The callback_function function is called when the interrupt occured.
"""	
import unittest		 
from nielvis import ButtonIRQ, IRQNumber

def irq_handler():
    print("Button interrupt is triggered. Now it is callback time.")

class Test_ButtonIRQ(unittest.TestCase):
    def test_OpenAndWait_DoesnotShowError(self):
        testcases = [
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': False, 'edge_count': 2},
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': True, 'edge_count': 2},
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': True, 'interrupt_type_falling': True, 'edge_count': 2},
        ]

        for testcase in testcases:
            with ButtonIRQ(irq_handler,
                           testcase['irq_number'],
                           testcase['timeout'],
                           testcase['interrupt_type_rising'],
                           testcase['interrupt_type_falling'],
                           testcase['edge_count'],) as button_irq:
                button_irq.wait()

class Test_ButtonIRQ_OpenAssertion(unittest.TestCase):
    def test_OpenWithInvalidInterruptType_ShowAssertion(self):
        testcases = [
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': 2}
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                button_irq = ButtonIRQ(irq_handler,
                                       testcase['irq_number'],
                                       testcase['timeout'],
                                       testcase['interrupt_type_rising'],
                                       testcase['interrupt_type_falling'],
                                       testcase['edge_count'])

    def test_OpenWithInvalidIrqNumber_ShowAssertion(self):
        invalid_irq_number = 0
        testcases = [
            {'irq_number': invalid_irq_number, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': 2}
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                button_irq = ButtonIRQ(irq_handler,
                                       testcase['irq_number'],
                                       testcase['timeout'],
                                       testcase['interrupt_type_rising'],
                                       testcase['interrupt_type_falling'],
                                       testcase['edge_count'])

    def test_OpenWithInvalidTimeout_ShowAssertion(self):
        invalid_timeout = -1
        testcases = [
            {'irq_number': IRQNumber.IRQ1, 'timeout': invalid_timeout, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': 2}
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                button_irq = ButtonIRQ(irq_handler,
                                       testcase['irq_number'],
                                       testcase['timeout'],
                                       testcase['interrupt_type_rising'],
                                       testcase['interrupt_type_falling'],
                                       testcase['edge_count'])

    def test_OpenWithInvalidEdgeCount_ShowAssertion(self):
        invalid_edge_counts = [0, 4294967296]
        testcases = [
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': invalid_edge_counts[0]},
            {'irq_number': IRQNumber.IRQ1, 'timeout': 6000, 'interrupt_type_rising': False, 'interrupt_type_falling': False, 'edge_count': invalid_edge_counts[1]},
        ]

        for testcase in testcases:
            with self.assertRaises(AssertionError):
                button_irq = ButtonIRQ(irq_handler,
                                       testcase['irq_number'],
                                       testcase['timeout'],
                                       testcase['interrupt_type_rising'],
                                       testcase['interrupt_type_falling'],
                                       testcase['edge_count'])
