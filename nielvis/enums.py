from pyvisa import constants
from enum import Enum, IntEnum

class Bank(Enum):
    """
    NI ELVIS III bank.

    Values:
        A: bank A
        B: bank B
    """
    A = 'A'
    B = 'B'

class AIChannel(IntEnum):
    """ NI ELVIS III Analog Input channel. """
    AI0 = 0
    AI1 = 1
    AI2 = 2
    AI3 = 3
    AI4 = 4
    AI5 = 5
    AI6 = 6
    AI7 = 7

class AOChannel(IntEnum):
    """ NI ELVIS III Analog Output channel. """
    AO0 = 0
    AO1 = 1

class DIOChannel(IntEnum):
    """ NI ELVIS III Digital Input and Output channel. """
    DIO0 = 0
    DIO1 = 1
    DIO2 = 2
    DIO3 = 3
    DIO4 = 4
    DIO5 = 5
    DIO6 = 6
    DIO7 = 7
    DIO8 = 8
    DIO9 = 9
    DIO10 = 10
    DIO11 = 11
    DIO12 = 12
    DIO13 = 13
    DIO14 = 14
    DIO15 = 15
    DIO16 = 16
    DIO17 = 17
    DIO18 = 18
    DIO19 = 19

class AIRange(Enum):
    """
    NI ELVIS III Analog Input range in volt.

    Values:
        PLUS_OR_MINUS_1V:
            Specifies the current allowed maximum value as 1V and minimum
            value as -1V for the channel.
        PLUS_OR_MINUS_2V:
            Specifies the current allowed maximum value as 2V and minimum
            value as -2V for the channel.
        PLUS_OR_MINUS_5V:
            Specifies the current allowed maximum value as 5V and minimum
            value as -5V for the channel.
        PLUS_OR_MINUS_10V:
            Specifies the current allowed maximum value as 10V and minimum
            value as -10V for the channel.
    """
    PLUS_OR_MINUS_1V = '+/-1V'
    PLUS_OR_MINUS_2V = '+/-2V'
    PLUS_OR_MINUS_5V = '+/-5V'
    PLUS_OR_MINUS_10V = '+/-10V'

class AIMode(Enum):
    """
    NI ELVIS III Analog Input mode.

    Values:
        NONE:
            Determines the voltage of a channel.
        DIFFERENTIAL:
            Determines the "differential" voltage between two separate
            channels.
    """
    SINGLE_ENDED = False
    DIFFERENTIAL = True

class EncoderChannel(IntEnum):
    """ NI ELVIS III Encoder channel. """
    ENC0 = 0
    ENC1 = 1
    ENC2 = 2
    ENC3 = 3
    ENC4 = 4
    ENC5 = 5
    ENC6 = 6
    ENC7 = 7
    ENC8 = 8
    ENC9 = 9

class EncoderMode(Enum):
    """
    NI ELVIS III Encoder mode.

    Values:
        QUADRATURE:
            Specifies that the encoder generates two phase signals that are
            offset by 90 degrees. The count value changes each time there is a
             falling or rising edge on either of the phases. Most encoders
             generate quadrature phase signals.
        STEP_AND_DIRECTION:
            Specifies that the encoder generates a direction signal and a
            clock signal. The direction signal determines the direction of the
            encoder. The count value changes on every rising edge of the clock
            signal.
    """
    QUADRATURE = 'quadrature'
    STEP_AND_DIRECTION = 'step and direction'

class UARTBaudRate(IntEnum):
    """ NI ELVIS III UART baud rate. """
    RATE110 = 110
    RATE300 = 300
    RATE600 = 600
    RATE1200 = 1200
    RATE2400 = 2400
    RATE4800 = 4800
    RATE9600 = 9600
    RATE19200 = 19200
    RATE38400 = 38400
    RATE57600 = 57600
    RATE115200 = 115200
    RATE230400 = 230400

class UARTDataBits(IntEnum):
    """ NI ELVIS III UART data bits. """
    BITS7 = 7
    BITS8 = 8

class UARTStopBits(Enum):
    """
    NI ELVIS III UART stop bits.

    Values:
        ONE: 1 stop bit
        TWO: 2 stop bits
    """
    ONE = constants.StopBits.one
    TWO = constants.StopBits.two

class UARTParity(Enum):
    """ NI ELVIS III UART parity. """
    NO = constants.Parity.none
    ODD = constants.Parity.odd
    EVEN = constants.Parity.even

class UARTFlowControl(Enum):
    """
    NI ELVIS III UART flow control.

    Values:
        NONE:
           The transfer mechanism does not use flow control. Buffers on both
           sides of the connection are assumed to be large enough to hold all
           data transferred.
        XOR_XOFF:
           The transfer mechanism uses the XON and XOFF characters to perform
           flow control. The transfer mechanism controls input flow by sending
           XOFF when the receive buffer is nearly full, and it controls the
           output flow by suspending transmission when XOFF is received.
        RTS_CTS:
           The transfer mechanism uses the XON and XOFF characters to perform
           flow control. The transfer mechanism controls input flow by sending
           XOFF when the receive buffer is nearly full, and it controls the
           output flow by suspending transmission when XOFF is received.
        DTR_DSR:
           The transfer mechanism uses the DTR output signal and the DSR input
           signal to perform flow control. The transfer mechanism controls
           input flow by unasserting the DTR signal when the receive buffer is
           nearly full, and it controls output flow by suspending the
           transmission when the DSR signal is unasserted.
    """
    NONE = constants.VI_ASRL_FLOW_NONE
    XOR_XOFF = constants.VI_ASRL_FLOW_XON_XOFF
    RTS_CTS = constants.VI_ASRL_FLOW_RTS_CTS
    DTR_DSR = constants.VI_ASRL_FLOW_DTR_DSR

class I2CSpeedMode(Enum):
    """
    NI ELVIS III I2C speed mode.

    Values:
        STANDARD: 100 kbps
        FAST: 400 kbps
    """
    STANDARD = 'STANDARD'
    FAST = 'FAST'

class SPIClockPhase(Enum):
    """
    NI ELVIS III SPI clock phase.

    Values:
        LEADING:
            The data is stable on the leading edge and changes on the trailing
            edge.
        TRAILING:
            The data is stable on the trailing edge and changes on the leading
            edge.
    """
    LEADING = 'Leading'
    TRAILING = 'Trailing'

class SPIClockPolarity(Enum):
    """
    NI ELVIS III SPI clock polarity.

    Values:
        LOW:
            The clock signal is low when idling, the leading edge is a rising
            edge, and the trailing edge is a falling edge.
        HIGH:
            The clock signal is high when idling, the leading edge is a
            falling edge, and the trailing edge is a rising edge.
    """
    LOW = 'Low'
    HIGH = 'High'

class SPIDataDirection(Enum):
    """
    NI ELVIS III SPI data direction.

    Values:
        LSB:
            Send the least significant bit first and the most significant bit
            last.
        MSB:
            Send the most significant bit first and the least significant bit
            last.
    """
    LSB = 'Least Significant Bit First'
    MSB = 'Most Significant Bit First'

class Led(IntEnum):
    """
    NI ELVIS III LED.

    Values:
        LED0:
            Enables state setting for LED0.
        LED1:
            Enables state setting for LED1.
        LED2:
            Enables state setting for LED2.
        LED3:
            Enables state setting for LED3.
    """
    LED0 = 0
    LED1 = 1
    LED2 = 2
    LED3 = 3

class IRQNumber(IntEnum):
    """ NI ELVIS III interrupt number. """
    IRQ1 = 1
    IRQ2 = 2
    IRQ3 = 3
    IRQ4 = 4
    IRQ5 = 5
    IRQ6 = 6
    IRQ7 = 7
    IRQ8 = 8

class AIIRQChannel(IntEnum):
    """ NI ELVIS III Analog Input Interrupt channel """
    AI0 = 0
    AI1 = 1

class AIIRQType(Enum):
    """
    NI ELVIS III Analog Input Interrupt type.

    Values:
        RISING:
            Register an interrupt on a rising edge of the analog input signal.
        FALLING:
            Register an interrupt on a falling edge of the analog input
            signal.
    """
    RISING = 'rising'
    FALLING = 'falling'

class DIIRQChannel(IntEnum):
    """ NI ELVIS III Digital Input Interrupt channel. """
    DIO0 = 0
    DIO1 = 1
    DIO2 = 2
    DIO3 = 3
