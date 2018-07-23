import time
import pyvisa
from nifpga import Session
import sys
sys.path.append('source/nielvisiii')
from enums import *

class ELVISIII(object):
    """ Register NI ELVIS III bitfile. """
    ResourceName = "RIO0"

    def __init__(self):
        self.session = Session("bitfile/ELVIS III v1.1 FPGA.lvbitx", ELVISIII.ResourceName)

    def __enter__(self):
        return self

    def close(self):
        self.session.close()

    def __exit__(self, exception_type, exception_val, trace):
        self.close()


class AnalogInput(ELVISIII):
    """ NI ELVIS III Analog Input (AI) API. """
    def __init__(self, *configuration):
        """
        Opens a session to one analog input channel or multiple analog input
        channels. Then, initialize analog input registration on NI ELVIS III.

        Args:
            *configuration (array):
                bank (Bank):specifies the name of the bank to open a session:
                    Specifies the name of the bank to open a session.
                channel (AIOChannel):
                    Specifies the names of the analog input channels to open a
                    session. When the mode is DIFFERENTIAL, the vaild AI
                    channels are AI0 to AI3.
                range (AIRange):
                    Specifies the minimum and maximum voltage, in volts, that
                    is allowed in the analog input channel or channels.The
                    default value is PLUS_OR_MINUS_10V which refers to +/-10V.
                mode (AIMode):
                    Specifies the mode used to read from analog input channels.
                    The default value is NONE.
        """
        # create a new AI session
        super(AnalogInput, self).__init__()

        # define a list to store all the necessary information for AI
        self.channel_list = []

        # define local variables which are used to track whether bank A and
        # bank B is used or is opened
        self.a_used = False
        self.b_used = False
        a_open = False
        b_open = False

        # initialize and store all channels within *configuration
        for configuration_details in configuration:
            # check that user inputted bank is correct
            assert configuration_details['bank'] in Bank

            # give default values for mode
            if 'mode' not in configuration_details:
                configuration_details['mode'] = AIMode.SINGLE_ENDED

            # check that user inputted channel is correct
            if configuration_details['mode'] == AIMode.SINGLE_ENDED:
                assert AIChannel.AI0 <= configuration_details['channel'] <= AIChannel.AI7
            elif configuration_details['mode'] == AIMode.DIFFERENTIAL:   # differential mode
                assert AIChannel.AI0 <= configuration_details['channel'] <= AIChannel.AI3, 'the valid range for channel is AI0 to AI3 in differential mode'

            # get valeus of Enum bank, channel, and mode
            configuration_details['bank'] = configuration_details['bank'].value
            configuration_details['channel'] = configuration_details['channel'].value
            configuration_details['mode'] = configuration_details['mode'].value

            # set the configuration value based on AI range
            if 'range' not in configuration_details:
                init_cnfg_value = 0
            else:
                assert configuration_details['range'] in AIRange
                init_range = configuration_details['range'].value
                if init_range == AIRange.PLUS_OR_MINUS_1V.value:
                    init_cnfg_value = int('110000', 2)
                elif init_range == AIRange.PLUS_OR_MINUS_2V.value:
                    init_cnfg_value = int('100000', 2)
                elif init_range == AIRange.PLUS_OR_MINUS_5V.value:
                    init_cnfg_value = int('10000', 2)
                elif init_range == AIRange.PLUS_OR_MINUS_10V.value:
                    init_cnfg_value = 0

            # save the detail information for the AI event into a array
            configuration = {'bank': Bank.A.value, 'channel': AIChannel.AI0.value, 'value': 0, 'cnfgval': init_cnfg_value}

            # get the bank A registration addresses and initialize them
            if configuration_details['bank'] == Bank.A.value and not a_open:

                # get registration addresses
                self.a_cnfg = self.session.registers['AI.A.CNFG']
                self.a_ready = self.session.registers['AI.A.VAL.RDY']
                self.a_cnt = self.session.registers['AI.A.CNT']
                self.a_cntr = self.session.registers['AI.A.CNTR']

                # congifure the AI channels to read
                self.a_cnfg.write([8,9,10,11,12,13,14,15,0,1,2,3])
                # regsiter the number of valid channels
                self.a_cnt.write(12)
                # register the analog sample rate
                # 1000 = 40MHz FPGA Clock Frequency / 40KHz (desired rate)
                # thus 1000 indicates 40KHz rate here
                self.a_cntr.write(1000)

                self.a_used = True
                a_open = True

            # get the bank B registration addresses and initialize them
            if configuration_details['bank'] == Bank.B.value and not b_open:

                # get registration addresses
                self.b_cnfg = self.session.registers['AI.B.CNFG']
                self.b_ready = self.session.registers['AI.B.VAL.RDY']
                self.b_cnt = self.session.registers['AI.B.CNT']
                self.b_cntr = self.session.registers['AI.B.CNTR']

                # congifure the AI channels to read
                self.b_cnfg.write([8,9,10,11,12,13,14,15,0,1,2,3])
                # regsiter the number of valid channels
                self.b_cnt.write(12)
                # register the analog sample rate
                # 1000 = 40MHz FPGA Clock Frequency / 40KHz (desired rate).
                # thus 1000 indicates 40KHz rate here.
                self.b_cntr.write(1000)

                self.b_used = True
                b_open = True

            configuration['bank'] = configuration_details['bank']
            configuration['channel'] = configuration_details['channel']
            configuration['mode'] = configuration_details['mode']
            self.channel_list.append(configuration)

    def read(self):
        """
        Reads values from one or more analog input channels. (1 sample)

        Returns:
            return_value (float array):
                Returns the value that this function reads from the analog
                input channel that you select.
        """
        # save the detail information for the AI event into a array
        # the information is different based on whether it is differential mode
        channel_list = []
        for channel in self.channel_list:
            configuration = {'bank': channel['bank'], 'channel': AIChannel.AI0.value, 'value': channel['value'], 'cnfgval': 0}
            if channel['mode']:
                # differential mode
                configuration['channel'] = 7 + channel['channel']
                configuration['value'] = self.session.registers['AI.DIFF_' + channel['bank'] + '_' + str(channel['channel']) + '.VAL']
                configuration['cnfgval'] = int(bin(channel['channel']), 2) | int('1000', 2) | channel['cnfgval']
            else:
                # single ended mode
                configuration['channel'] = 7 + channel['channel']
                configuration['value'] = self.session.registers['AI.' + channel['bank'] + '_' + str(channel['channel']) + '.VAL']
                configuration['cnfgval'] = int(bin(channel['channel']), 2) | int('1000', 2) | channel['cnfgval']
            channel_list.append(configuration)

        # define local variables
        a_current_cnfg = ""
        b_current_cnfg = ""
        a_check = False
        b_check = False

        # set the current configuration for all channels within channel_list
        for channel in channel_list:
            if channel['bank'] == Bank.A.value:
                # set bank A registration and the local variable of it
                a_current_cnfg = self.a_cnfg.read()
                a_current_cnfg[channel['channel']] = channel['cnfgval']
                a_check = True
            else:
                # set bank B registration and the local variable of it
                b_current_cnfg = self.b_cnfg.read()
                b_current_cnfg[channel['channel']] = channel['cnfgval']
                b_check = True

        # set the configure registration for all bank A
        if a_check:
            self.a_cnfg.write(a_current_cnfg)
            stop = True
            while stop:
                check = self.a_cnfg.read()
                if a_current_cnfg == check and self.a_ready.read():
                    stop = False

        # set the configure registration for all bank B
        if b_check:
            self.b_cnfg.write(b_current_cnfg)
            stop = True
            while stop:
                check = self.b_cnfg.read()
                if b_current_cnfg == check and self.b_ready.read():
                    stop = False

       # append all the read back values and return the array
        return_value = []
        for channellist_details in channel_list:
            return_value.append(float(channellist_details['value'].read()))
        return return_value

    def toBinary(self, num):
        return bin(int(num))


class AnalogOutput(ELVISIII):
    """ NI ELVIS III Analog Output (AO) API. """
    def __init__(self, *configuration):
        """
        Opens a session to one analog output channel or multiple analog output
        channels. Then, initialize analog output registration on NI ELVIS III.

        Args:
            *configuration (array):
                bank (Bank):
                    Specifies the name of the bank to open a session.
                channel (AIOChannel):
                    Specifies the names of the analog output channels to open
                    a session. The valid value of analog output channel is AO0
                    and AO1.
        """
        super(AnalogOutput, self).__init__()
        self.channel_list = []
        channel_value = {'value': '0'}
        for configuration_details in configuration:
            assert configuration_details['bank'] in Bank
            assert AOChannel.AO0 <= configuration_details['channel'] <= AOChannel.AO1
            configuration_details['bank'] = configuration_details['bank'].value
            configuration_details['channel'] = configuration_details['channel'].value
            self.value = self.session.registers['AO.' + configuration_details['bank'] + '_' + str(configuration_details['channel']) + '.VAL']
            self.go = self.session.registers['AO.SYS.GO']
            self.stat = self.session.registers['AO.SYS.STAT']
            self.lsb_weights = 4882813.0 / 1E+9
            self.offset = 0.0 / 1E+9
            self.signed = True
            self.enamask = configuration_details['channel']^2
            channel_value['value'] = self.value
            self.channel_list.append(channel_value['value'])

    def write(self, value):
        """
        Writes values to one or more analog output channels. (1 sample)

        Args:
            value (float):
                Specifies the value, in volts, to write to the analog output
                channels. The value must be in the range of +/-10. If you
                specify a value that is invalid, this function coerces the
                specified value to the nearest valid value when you execute
                the program.
        """
        for channel in self.channel_list:
            stat_value = self.stat.read()
            self.value = channel
            self.value.write(value)
            self.go.write(True)
            stat_current = stat_value
            while stat_current == stat_value:
                stat_current = self.stat.read()
            self.go.write(False)


class DigitalInputOutput(ELVISIII):
    """ NI ELVIS III Digital Input and Output (DIO) API. """
    def __init__(self, bank=Bank.A):
        """
        Opens a session to one or more digital input and output channels.
        Then, initialize digital I/O registration on NI ELVIS III.

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session. The default
                value is A.
        """
        super(DigitalInputOutput, self).__init__()
        assert bank in Bank
        bank = bank.value
        self.write_registration = self.session.registers['DIO.' + bank + '_19:0.OUT']
        self.read_registration = self.session.registers['DIO.' + bank + '_19:0.IN']
        self.direction = self.session.registers['DIO.' + bank + '_19:0.DIR']
        self.direction.write(0x00)

    def to_write(self, *channels):
        """
        Changes direction of the digital I/O channels to the write direction.
        This function is used internally and should not be used in other
        examples.

        Args:
            *channels (DIOChannel):
                Specifies the names of the digital I/O channels. This value
                can be a single channel (ex: 7) or a list of channels
                (ex: 7, 8 ,9).
        """
        dir = int('00000000000000000000', 2)
        for channel in channels[0]:
            assert DIOChannel.DIO0 <= channel <= DIOChannel.DIO19
            channel = channel.value
            dir |= (1 << channel)
        self.direction.write(dir)

    def read(self, *channels):
        """
        Reads the logic levels of one or more digital I/O channels. (1 sample)

        Args:
            *channels (DIOChannel):
                Specifies the names of the digital I/O channels to read from.
                This value can be a single channel (ex: 7) or a list of
                channels (ex: 7, 8 ,9).

        Returns:
            return_value (int array):
                Returns the value that this function reads from the digital
                input channel that you select.
        """
        return_value = []
        value = self.read_registration.read()
        for channel in channels:
            assert DIOChannel.DIO0 <= channel <= DIOChannel.DIO19
            channel = channel.value
            return_value.append(int(0 < (int(value) & (1 << channel))))
        return return_value

    def write(self, value, *channels):
        """
        Write the value to all channels initialized. (1 sample)

        Args:
            value (bool):
                Specifies the logic levels to write to the digital I/O
                channels. Set value to TRUE to write a high voltage and set
                value to FALSE to write a low voltage. The direction of a
                channel automatic changes to output before this function
                writes the logic level. You must specify a value for channels
                that you open.
            *channels (DIOChannel):
                Specifies the names of the digital I/O channels to write to.
                This value can be a single channel (ex: 7) or a list of
                channels (ex: 7, 8 ,9).
        """
        assert type(value) == bool
        self.to_write(channels)
        value = int(value)
        write_values = int('0000000000000000000', 2)
        for channel in channels:
            assert DIOChannel.DIO0 <= channel <= DIOChannel.DIO19
            channel = channel.value
            write_values |= (value << channel)
        self.write_registration.write(write_values)


class Encoder(ELVISIII):
    """ NI ELVIS III Encoder API. """
    def __init__(self, bank=Bank.A,
                       channel=EncoderChannel.ENC0,
                       encoder_mode=EncoderMode.QUADRATURE):
        """
        Opens a session to an encoder channel and initialize the Encoder
        registration on NI ELVIS III.

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session. The default
                value is A.
            channel (EncoderChannel):
                Specifies the name of the encoder channel whose session you
                want to open. The default value is encoder channel ENC0.
            encoder_mode (EncoderMode):
                Specifies the type of output signal from the encoder you use.
                The default value is QUADRATURE.
        """
        super(Encoder, self).__init__()
        assert bank in Bank
        assert EncoderChannel.ENC0 <= channel <= EncoderChannel.ENC9
        assert encoder_mode in EncoderMode
        bank = bank.value
        channel = channel.value
        self.cnfg = self.session.registers['ENC.' + bank + '_' + str(channel) + '.CNFG']
        self.cntr = self.session.registers['ENC.' + bank + '_' + str(channel) + '.CNTR']
        self.stat = self.session.registers['ENC.' + bank + '_' + str(channel) + '.STAT']
        self.sys_select = self.session.registers['SYS.SELECT' + bank]

        if encoder_mode == EncoderMode.QUADRATURE:
            self.cnfg.write(int('00000001', 2))
        else:
            self.cnfg.write(int('00000101', 2))

        select = self.sys_select.read()
        select |= (1 << (channel*4 + 1))
        self.sys_select.write(select)

    def read(self, reset_counter=False):
        """
        Reads the value of the encoder tick counter and the last direction of
        the tick counter.

        Args:
            reset_counter (bool):
                Specifies whether to reset the tick counter to zero after this
                function runs. The default is False.

        Returns:
            counter_value (int):
                Returns the number of ticks that this function reads from the
                encoder since the last counter reset. Counter Value must be in
                the range from -2,147,483,648 to 2,147,483,647.
            direction_decrease (bool):
                Returns the direction of the counter between the last two
                ticks that the encoder receives.
        """
        assert type(reset_counter) == bool
        counter_value = self.cntr.read()
        counter_value = counter_value & 0xffffffff
        counter_value = counter_value | (-(counter_value & 0x80000000))
        stat = self.stat.read()
        direction_decrease = stat & 0x01
        error = stat & 0x02
        signed_overflow = stat & 0x08
        signed_overflow_error = stat & 0x20
        cnfg_to_write = int('00000000', 2)
        cnfg_to_write |= int(signed_overflow | signed_overflow_error) << 4
        cnfg_to_write |= int(error) << 3
        reset_number = 0
        if reset_counter:
            reset_number = 1 << 1
            reset_number |= cnfg_to_write
            current_cnfg = self.cnfg.read()
            first_cnfg = reset_number | current_cnfg
            self.cnfg.write(first_cnfg)
            self.cnfg.write(~reset_number & current_cnfg)
        if signed_overflow_error or error:
            if error:
                raise OverflowError('An invalid transition occurred in the quadrature mode.')
            else:
                raise OverflowError('Signed Overflow Error. This occurred in the encoder counter while the overflow flag was still set.')
        return counter_value, direction_decrease


class PWM(ELVISIII):
    """ NI ELVIS III Pulse Width Modulation (PWM) API. """
    def __init__(self, bank=Bank.A, channel=DIOChannel.DIO0):
        """
        Opens a session to a pulse width modulation (PWM) channel and
        initialize PWM registration on NI ELVIS III.

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session. The default
                is A.
            *channels (DIOChannel):
                Specifies the name of the PWM channel to open a session. The
                default is DIO0.
        """
        super(PWM, self).__init__()
        assert bank in Bank
        assert DIOChannel.DIO0 <= channel <= DIOChannel.DIO19
        bank = bank.value
        channel = channel.value
        self.cs = self.session.registers['PWM.' + bank + '_' + str(channel) + '.CS']
        self.cnfg = self.session.registers['PWM.' + bank + '_' + str(channel) + '.CNFG']
        self.cmp = self.session.registers['PWM.' + bank + '_' + str(channel) + '.CMP']
        self.max = self.session.registers['PWM.' + bank + '_' + str(channel) + '.MAX']
        self.cntr = self.session.registers['PWM.' + bank + '_' + str(channel) + '.CNTR']
        self.sys_select = self.session.registers['SYS.SELECT' + bank]
        select = self.sys_select.read()
        select |= (1 << (channel*2))
        self.sys_select.write(select)

    def generate(self, frequency, duty_cycle):
        """
        Sets the duty cycle value and frequency value of a pulse width
        modulation (PWM) signal.

        Args:
            frequency (int):
                Specify the frequency of the PWM signal in hertz. Frequency
                must be within the range of 40 Hz to 40 kHz.
            duty_cycle (float):
                Specifies the percentage of time the PWM signal remains high
                over one PWM cycle. Valid values must be within the range
                [0:1].
        """
        assert 40 <= frequency <= 400000 and type(frequency) == int
        assert 0 <= duty_cycle <= 1
        clock_divisors = [1, 2, 4, 8, 16, 32, 64]
        actual_frequency, top, clock_divisor = calculate_clock_settings(frequency, clock_divisors)
        pwm_cs = 0
        for divisor in clock_divisors:
            if divisor == clock_divisor:
                break
            pwm_cs += 1
        pwm_cs += 1
        pwm_max = top
        pwm_cnfg = int('00000100', 2)
        self.cmp.write(int(duty_cycle * pwm_max))
        self.max.write(int(pwm_max))
        self.cnfg.write(int(pwm_cnfg))
        self.cs.write(int(pwm_cs))


class LEDs(ELVISIII):
    """ NI ELVIS III LED API. """
    def __init__(self):
        """
        Open the session to LED and initialize LED registration on NI ELVIS
        III.
        """
        super(LEDs, self).__init__()
        self.leds = self.session.registers['DO.LED3:0']

    def write(self, led=Led.LED0, value_to_set=True):
        """
        Sets the states of the LEDs.

        Args:
            led (Led):
                Specifies the name for the led to select. The default value is
                LED0.
            value_to_set (bool):
                Specifies the states of the led. The defult is True which
                turns the LED on.
        """
        assert Led.LED0 <= led <= Led.LED3
        assert type(value_to_set) == bool
        value = self.leds.read()
        if led == Led.LED0:
            value = (value & int('1110', 2))
            if value_to_set:
                value = value | 0x01
        elif led == Led.LED1:
            value = (value & int('1101', 2))
            if value_to_set:
                value = value | 0x02
        elif led == Led.LED2:
            value = (value & int('1011', 2))
            if value_to_set:
                value = value | 0x04
        elif led == Led.LED3:
            value = (value & int('0111', 2))
            if value_to_set:
                value = value | 0x08
        self.leds.write(value)


class I2C(ELVISIII):
    """ NI ELVIS III Inter-Integrated Circuit (I2C) API. """
    def __init__(self, bank=Bank.A, mode=I2CSpeedMode.STANDARD):
        """
        Opens a session to an Inter-Integrated Circuit (I2C) channel and
        initialize I2C registration on NI ELVIS III.

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session. The default
                value is A.
            mode (I2CSpeedMode):
                Specifies the user-configurable properties of the I2C channel.
                The default value is STANDARD.
        """
        super(I2C, self).__init__()
        assert bank in Bank
        assert mode in I2CSpeedMode
        bank = bank.value
        self.sys_select = self.session.registers['SYS.SELECT' + bank]
        self.cntr = self.session.registers['I2C.' + bank + '.CNTR']
        self.cnfg = self.session.registers['I2C.' + bank + '.CNFG']
        self.addr = self.session.registers['I2C.' + bank + '.ADDR']
        self.cntl = self.session.registers['I2C.' + bank + '.CNTL']
        self.dato = self.session.registers['I2C.' + bank + '.DATO']
        self.go = self.session.registers['I2C.' + bank + '.GO']
        self.stat = self.session.registers['I2C.' + bank + '.STAT']
        self.dati = self.session.registers['I2C.' + bank + '.DATI']
        self.configure(mode)

    def configure(self, mode):
        """
        Configures the transfer rate of an Inter-Integrated Circuit (I2C)
        channel based on the input I2C session. This function is used
        internally and should not be used in other examples.

        Args:
            mode (I2CSpeedMode):
                Specifies the user-configurable properties of the I2C channel.
                The default value is STANDARD.
        """
        assert mode in I2CSpeedMode
        if mode == I2CSpeedMode.STANDARD:
            self.cntr.write(213 & 0xFF)
        else:
            self.cntr.write(63 & 0xFF)
        self.cnfg.write(1 & 0xFF)

        read_sysselect = self.sys_select.read()
        self.sys_select.write(read_sysselect | int('1111000000000000000000000000000', 2))

    def write(self, slave_address, bytes_to_write, keep_bus_busy=True, timeout_ms=1000):
        """
        Write to a specified slave device based on the address and keep the
        bus busy if needed.

        Args:
            slave_address (int):
                Specifies the address of the slave device to which this
                function writes data. You must specify the address in 7-bit.
                Some I2C devices might have a 8-bit address in which the first
                7 bits represent the address and the last bit represents the
                mode of operation. For these kinds of I2C devices, you must
                specify Slave Address (7-bit) using the seven most significant
                bits. slave_address must be written in hex format.
            bytes_to_write (int array):
                Specifies the data to write to the I2C slave device.
            keep_bus_busy (bool):
                Specifies whether to keep the I2C channel open so that you can
                perform additional operations. For example, if a slave device
                requires a write operation followed by a read operation to
                perform a command, you must set Keep Bus Busy to True. The
                default is True.
            timeout_ms (int):
                Specifies the number of milliseconds this VI waits for writing
                a single byte before timing out. The default is 1000.
        """
        assert 0 <= slave_address <= 127, "You must specify the slave address using the seven most significant bits (MSB) to 7 bit."
        assert bytes_to_write >= 0
        self.addr.write(slave_address << 1)
        timeout = False
        error = False
        for n in range(0, len(bytes_to_write)):
            if len(bytes_to_write) == 1:
                if keep_bus_busy:
                    cntl_to_send = int('00000011', 2)
                else:
                    cntl_to_send = int('00000111', 2)
            else:
                if n == 0:
                    cntl_to_send = int('00000011', 2)
                else:
                    if ((len(bytes_to_write) - 1) == n) and not keep_bus_busy:
                        cntl_to_send = int('00000101', 2)
                    else:
                        cntl_to_send = int('00000001', 2)
            self.cntl.write(cntl_to_send)
            self.dato.write(bytes_to_write[n])
            self.go.write(True)
            start_time = time.time()
            n = True
            while n:
                if not timeout_ms < 0:
                    if (time.time() - start_time) >= timeout_ms:
                        timeout = True
                i2c_stat = self.stat.read()
                if ((i2c_stat & int('00000001', 2)) == 0) or timeout:
                    n = False
            if timeout:
                error = True
            else:
                if (i2c_stat & int('00000010', 2)) == int('00000010', 2):
                    if (i2c_stat & int('00000100', 2)) == int('00000100', 2):
                        raise ValueError('A No Acknowledge (NAK) bit was received from the slave device after the last address transmission.')
                        error = True
                    else:
                        raise ValueError('A No Acknowledge (NAK) bit was received from the slave device after the last data transmission.')
                        error = True
            if error and not keep_bus_busy:
                self.cntl.write(int('00000101', 2))

    def read(self, slave_address, num_bytes_to_read, keep_bus_busy=False, timeout_ms=1000):
        """
        Read a specified number of bytes from the slave device based on the
        address.

        Args:
            slave_address (int):
                Specifies the address of the slave device to which this
                function writes data. You must specify the address in 7-bit.
                Some I2C devices might have a 8-bit address in which the first
                7 bits represent the address and the last bit represents the
                mode of operation. For these kinds of I2C devices, you must
                specify Slave Address (7-bit) using the seven most significant
                bits. slave_address must be written in hex format.
            num_bytes_to_read (int):
                Specifies the number of bytes of data reads from the I2C slave
                device.
            keep_bus_busy (bool):
                Specifies whether to keep the I2C channel open so that you can
                perform additional operations. For example, if a slave device
                requires a write operation followed by a read operation to
                perform a command, you must set Keep Bus Busy to True. The
                default is False.
            timeout_ms (int):
                Specifies the number of milliseconds this VI waits for writing
                a single byte before timing out. The default is 1000.

        Returns:
            return_value (int array):
                Returns the data that this function reads from the I2C slave
                device.
        """
        assert 0 <= slave_address <= 127, "You must specify the slave address using the seven most significant bits (MSB) to 7 bit."
        assert num_bytes_to_read >= 0
        return_value = []
        error = False
        timeout = False
        self.addr.write(slave_address << 1 | 1)
        for n in range(0, num_bytes_to_read):
            if num_bytes_to_read == 1:
                if keep_bus_busy:
                    cntl_to_send = int('00001011', 2)
                else:
                    cntl_to_send = int('00000111', 2)
            else:
                if n == 0:
                    cntl_to_send = int('00001011', 2)
                else:
                    if (num_bytes_to_read - 1) == n:
                        if keep_bus_busy:
                            cntl_to_send = int('00001001', 2)
                        else:
                            cntl_to_send = int('00000101', 2)
                    else:
                        cntl_to_send = int('00001001', 2)
            self.cntl.write(cntl_to_send)
            self.go.write(True)
            start_time = time.time()
            n = True
            while n:
                if not timeout_ms < 0:
                    if (time.time() - start_time) >= timeout_ms:
                        timeout = True
                i2c_stat = self.stat.read()
                if ((i2c_stat & int('00000001', 2)) == 0) or timeout:
                    n = False
            if timeout:
                error = True
            else:
                if (i2c_stat & int('00000010', 2)) == int('00000010', 2):
                    raise ValueError('A No Acknowledge (NAK) bit was received from the slave device after the last address transmission.')
                    error = True
                else:
                    return_value.append(self.dati.read())
            if error and not keep_bus_busy:
                self.cntl.write(int('00000101', 2))
        return return_value


class SPI(ELVISIII):
    """ NI ELVIS III Serial Peripheral Interface Bus (SPI) API. """
    def __init__(self, frequency,
                       bank=Bank.A,
                       clock_phase=SPIClockPhase.LEADING,
                       clock_polarity=SPIClockPolarity.LOW,
                       data_direction=SPIDataDirection.MSB,
                       frame_length=8):
        """
        Open the session to a serial peripheral interface (SPI) channel and
        disables the SPI channels and resets the configuration of the channels.

        Args:
            frequency (int):
                Specifies the frequency of the generated clock signal.
            bank (Bank):
                Specifies the name of the bank whose session you want to open.
                The default value is A.
            clock_phase (SPIClockPhase):
                Specifies the clock phase at which the data remains stable in
                the SPI transmission cycle. The default value is LEADING.
            clock_polarity (SPIClockPolarity):
                Specifies the base level of the clock signal and the logic
                level of the leading and trailing edges. The default value is
                LOW.
            data_direction (SPIDataDirection):
                Specifies the order in which the bits in the SPI frame are
                transmitted. The default value is MSB.
            frame_length (int):
                Specifies the number of frames that make up a single SPI
                transmission. Frame Length can be a value from 3 to 15, which
                specifies a frame length of 4 to 16. The default value is 8.
        """
        super(SPI, self).__init__()
        assert 40 <= frequency <= 4000000
        assert 4 <= frame_length <= 16
        assert bank in Bank
        assert clock_phase in SPIClockPhase
        assert clock_polarity in SPIClockPolarity
        assert data_direction in SPIDataDirection
        with DigitalInputOutput(bank) as dio:
            dio.to_write({DIOChannel.DIO0})
        bank = bank.value
        clock_phase = clock_phase.value
        clock_polarity = clock_polarity.value
        data_direction = data_direction.value
        self.sys_select = self.session.registers['SYS.SELECT' + bank]
        self.cnt = self.session.registers['SPI.' + bank + '.CNT']
        self.cnfg = self.session.registers['SPI.' + bank + '.CNFG']

        self.go = self.session.registers['SPI.' + bank + '.GO']
        self.dato = self.session.registers['SPI.' + bank + '.DATO']
        self.dati = self.session.registers['SPI.' + bank + '.DATI']
        self.bank = bank
        self.configure(frequency, clock_phase, clock_polarity, data_direction, frame_length)

    def configure(self, frequency, clock_phase, clock_polarity, data_direction, frame_length):
        """
        Set up the SPI configuration on NI ELVIS III. This function is used
        internally and should not be used in other examples.

        Args:
            frequency (int):
                Specifies the frequency of the generated clock signal.
            clock_phase (SPIClockPhase):
                Specifies the clock phase at which the data remains stable in
                the SPI transmission cycle.
            clock_polarity (SPIClockPolarity):
                Specifies the base level of the clock signal and the logic
                level of the leading and trailing edges.
            data_direction (SPIDataDirection):
                Specifies the order in which the bits in the SPI frame are
                transmitted.
            frame_length (int):
                Specifies the number of frames that make up a single SPI
                transmission. Frame Length can be a value from 3 to 15, which
                specifies a frame length of 4 to 16.
        """
        spi_cnfg = int('0000000000000000',2)
        if clock_phase != SPIClockPhase.LEADING.value:
            spi_cnfg = spi_cnfg | (1 << 1)
        if clock_polarity != SPIClockPolarity.LOW.value:
            spi_cnfg = spi_cnfg | (1 << 2)
        if data_direction != SPIDataDirection.MSB.value:
            spi_cnfg = spi_cnfg | (1 << 3)
        spi_cnfg = spi_cnfg | ((frame_length-1) << 4)
        clock_divisors = [1, 2, 4, 8]
        actual_frequency, top, clock_divisor = calculate_clock_settings(frequency, clock_divisors, 4000000, 40, 20000000,
                                                                        65535, 1, True, True)
        index = 0
        for clock_number in clock_divisors:
            if clock_number == clock_divisor:
                break
            index += 1
        spi_cnfg = spi_cnfg | (index << 14)
        self.cnfg.write(spi_cnfg & 0xFFFF)
        self.cnt.write(int(top) & 0xFFFF)

        read_system_select = self.sys_select.read()
        self.sys_select.write(read_system_select | int('111111000000000', 2))
        return

    def read(self, bytes_count):
        """
        Read a specified number of frames from a SPI channel.

        Args:
            bytes_count (int):
                Specifies the number of bytes to read from the SPI channel.

        Returns:
            bytes_to_read (string array):
                Returns the data that this function reads from the SPI
                channel. The length of data is based on bytes_count.
        """
        assert type(bytes_count) == int and bytes_count >= 0
        bytes_to_read = []
        for byte in range(bytes_count):
            bytes_to_read.append(0)
        return self.writeread(bytes_to_read)

    def write(self, bytes_to_write):
        """
        Writes data to a SPI channel.

        Args:
            bytes_to_write (int):
                Specifies the data to write to the SPI channel. It should be
                written in hex format.
        """
        self.writeread(bytes_to_write)

    def writeread(self, bytes_to_write):
        """
        Writes and reads data through a SPI channel at the same time. The
        number of data frames to write equals the number of the data frames to
        read.

        Args:
            bytes_to_write (int):
                Specifies the data to write to the SPI channel. It should be
                written in hex format.

        Returns:
            bytes_to_read (string array):
                Returns the data that this function reads from the SPI
                channel. The length of data is based on bytes_count.
        """
        bytes_to_read = []
        for byte in bytes_to_write:
            self.dato.write(byte)
            self.go.write(True)

            if self.bank == Bank.A.value:
                irq = 27
            else:
                irq = 26
            irq_status = self.session.wait_on_irqs(irq, -1)
            self.session.acknowledge_irqs(irq_status.irqs_asserted)
            bytes_to_read.append(hex(self.dati.read()).split('x')[-1])

        return bytes_to_read


class IRQ(ELVISIII):
    def __init__(self):
        super(IRQ, self).__init__()

    def irq_wait(self, timeout, irq_number=0):
        """
        Either trigger the interrupt or timeout. This function is used
        internally and should not be used in non-interrupt examples.

        Args:
            timeout (int):
                Specifies the amount of time for timeout when interrupt is not
                triggered. The default value is 10000.
            irq_number (int):
                Specifies the identifier of the interrupt to register. The
                valid values are 0 and IRQ1 to IRQ7. The default value is 0
                which is only used by timer interrupt. The valid range for
                other interrupts are from IRQ1 to IRQ7.  
        """
        assert timeout >= 0
        assert 0 <= irq_number <= IRQNumber.IRQ8
        print "waiting for IRQ..."
        irq_status = self.session.wait_on_irqs([irq_number], timeout)
        if irq_number in irq_status.irqs_asserted:
            print irq_number, "was asserted. IRQ occured."
            self.callback_function()
            self.acknowledge(irq_number)
        else:
            print irq_number, "was not asserted. Timeout."

    def acknowledge(self, irq_number):
        """
        Acknowledges an IRQ or set of IRQs. This function is used internally
        and should not be used in non-interrupt examples.

        Args:
            irq_number (int):
                Specifies the identifier of the interrupt to register. The
                valid values are 0 and IRQ1 to IRQ7. The default value is 0
                which is only used by timer interrupt. The valid range for
                other interrupts are from IRQ1 to IRQ7.
        """
        assert 0 <= irq_number <= IRQNumber.IRQ8
        irq_status = self.session.wait_on_irqs([irq_number], 0)
        while irq_number in irq_status.irqs_asserted:
            time.sleep(0.5)
            self.session.acknowledge_irqs(irq_status.irqs_asserted)
            irq_status = self.session.wait_on_irqs([irq_number], 0)


class ButtonIRQ(IRQ):
    """
    NI ELVIS III Button Interrupt (ButtonIRQ) API.
    """
    def __init__(self,
                 callback_function,
                 irq_number=IRQNumber.IRQ1,
                 timeout=10000,
                 type_rising=True,
                 type_falling=False,
                 edge_count=1):
        """
        Open a session to register button interrupt.
        
        Args:
            callback_function (function):
                Specifies the reference to a callback function.
            irq_number (IRQNumber):
                Specifies the identifier of the interrupt to register. The
                valid values are within the range IRQ1 to IRQ7. You cannot
                register an I/O interrupt with the same IRQ number as a
                registered I/O interrupt. However, after you closed the
                existing interrupt, you can use the IRQ number to register
                another interrupt. The default value is IRQ1.
            timeout (int):
                Specifies the amount of time for timeout when interrupt is not
                triggered. The default value is 10000.
            type_rising (bool):
                Specifies to register an interrupt on the rising edge of the
                digital input signal. The default value is True.
            type_falling (bool):
                Specifies to register an interrupt on the falling edge of the
                digital input signal. The default value is False.
            edge_count (int):
                specifies the edge number of the digital input signal that
                must occur for this function to register an interrupt. The
                default is 1. The range of edge_count is from 1 to 4294967295.
        """
        super(ButtonIRQ, self).__init__()
        assert callable(callback_function), "callback_function need to be a function"
        assert IRQNumber.IRQ1 <= irq_number <= IRQNumber.IRQ8
        assert timeout >= 0
        if type_rising == type_falling:
            assert type_falling != False
        assert 1 <= edge_count <= 4294967295
        irq_num = self.session.registers['IRQ.DI_BTN.NO']
        enable = self.session.registers['IRQ.DI_BTN.ENA']
        rise = self.session.registers['IRQ.DI_BTN.RISE']
        fall = self.session.registers['IRQ.DI_BTN.FALL']
        counter = self.session.registers['IRQ.DI_BTN.CNT']
        self.timeout = timeout
        self.callback_function = callback_function
        self.irq_number = irq_number.value
        irq_num.write(self.irq_number)
        counter.write(edge_count)
        enable.write(True)
        rise.write(type_rising)
        fall.write(type_falling)

    def wait(self):
        """
        Configure ButtonIRQ and execute the interrupt events.
        """
        self.acknowledge(self.irq_number)
        self.irq_wait(self.timeout, self.irq_number)


class DIIRQ(IRQ):
    """
    NI ELVIS III Digital Input Interrupt (DIIRQ) API.
    """
    def __init__(self,
                 channel,
                 callback_function,
                 irq_number=IRQNumber.IRQ1,
                 timeout=10000,
                 type_rising=True,
                 type_falling=False,
                 edge_count=1):
        """
        Initialize DIIRQ registration.

        Args:
            channel (DIIRQChannel)
            callback_function (function):
                Specifies the reference to a callback function.
            irq_number (IRQNumber):
                Specifies the identifier of the interrupt to register. The
                valid values are within the range IRQ1 to IRQ7. You cannot
                register an I/O interrupt with the same IRQ number as a
                registered I/O interrupt. However, after you closed the
                existing interrupt, you can use the IRQ number to register
                another interrupt. The default value is IRQ1.
            timeout (int):
                Specifies the amount of time for timeout when interrupt is not
                triggered. The default value is 10000.
            type_rising (bool):
                Specifies to register an interrupt on the rising edge of the
                digital input signal. The default value is True.
            type_falling (bool):
                Specifies to register an interrupt on the falling edge of the
                digital input signal. The default value is False.
            edge_count (int):
                specifies the edge number of the digital input signal that
                must occur for this function to register an interrupt. The
                default is 1. The range of edge_count is from 1 to 4294967295.
        """
        super(DIIRQ, self).__init__()
        assert DIIRQChannel.DIO0 <= channel <= DIIRQChannel.DIO3
        assert callable(callback_function), "callback_function need to be a function"
        assert IRQNumber.IRQ1 <= irq_number <= IRQNumber.IRQ8
        assert timeout >= 0
        if type_rising == type_falling:
            assert type_falling != False
        assert 1 <= edge_count <= 4294967295
        channel = channel.value
        enable = self.session.registers['IRQ.DIO_A_7:0.ENA']
        rise = self.session.registers['IRQ.DIO_A_7:0.RISE']
        fall = self.session.registers['IRQ.DIO_A_7:0.FALL']
        counter = self.session.registers['IRQ.DIO_A_' + str(channel) + '.CNT']
        irq_num = self.session.registers['IRQ.DIO_A_' + str(channel) + '.NO']

        counter.write(edge_count)
        rise_value = rise.read()
        rise.write(rise_value | (int(type_rising) << channel))
        fall_value = fall.read()
        fall.write(fall_value | (int(type_falling) << channel))
        enable_value = enable.read()
        enable.write(enable_value | (1 << channel))

        self.callback_function = callback_function
        self.timeout = timeout
        self.irq_number = irq_number.value
        irq_num.write(self.irq_number)

    def wait(self):
        """
        Configure DIIRQ and execute the interrupt events.
        """
        self.acknowledge(self.irq_number)
        self.irq_wait(self.timeout, self.irq_number)


class AIIRQ(IRQ):
    """
    NI ELVIS III Analog Input Interrupt (AIIRQ) API.
    """
    def __init__(self,
                 channel,
                 callback_function,
                 irq_number=IRQNumber.IRQ1,
                 timeout=10000,
                 threshold=2.5,
                 hysteresis=0.02,
                 irq_type=AIIRQType.RISING):
        """
        Initialize AIIRQ registration.

        Args:
            channel (AIIRQChannel)
            callback_function (function):
                Specifies the reference to a callback function.
            irq_number (IRQNumber):
                Specifies the identifier of the interrupt to register. The
                valid values are within the range IRQ1 to IRQ7. You cannot
                register an I/O interrupt with the same IRQ number as a
                registered I/O interrupt. However, after you closed the
                existing interrupt, you can use the IRQ number to register
                another interrupt. The default value is IRQ1.
            timeout (int):
                Specifies the amount of time for timeout when interrupt is not
                triggered. The default value is 10000.
            threshold (float):
                Specifies the value, in volts, that the analog input signal
                must cross for this function to register an interrupt. The
                ragne of threshold is from 0 to 5. The default value is 2.5.
            hysteresis (float):
                Specifies a window, in volts, above or below threshold. You do
                not need to change the value for this input unless you notice
                a false interrupt registration. The range is from 0 to 1. The
                default value is 0.02.
            type (AIIRQType):
                Specifies when to register the interrupt based on the analog
                input signal. The default value is RISING.
        """
        super(AIIRQ, self).__init__()
        assert channel == AIIRQChannel.AI0 or channel == AIIRQChannel.AI1
        assert callable(callback_function), "callback_function need to be a function"
        assert IRQNumber.IRQ1 <= irq_number <= IRQNumber.IRQ8
        assert timeout >= 0
        assert 0 <= threshold <= 5
        assert 0 <= hysteresis <= 1
        assert irq_type == AIIRQType.RISING or irq_type == AIIRQType.FALLING
        self.ai = AnalogInput({'bank': Bank.A, 'channel': channel})
        channel = channel.value
        irq_num = self.session.registers['IRQ.AI_A_' + str(channel) + '.NO']
        irq_hysteresis = self.session.registers['IRQ.AI_A_' + str(channel) + '.HYSTERESIS']
        irq_threshold = self.session.registers['IRQ.AI_A_' + str(channel) + '.THRESHOLD']
        cnfg = self.session.registers['IRQ.AI_A.CNFG']
        irq_number = irq_number.value
        irq_type = irq_type.value
        irq_num.write(irq_number)
        irq_threshold.write(threshold)
        irq_hysteresis.write(hysteresis)

        cnfg_value = cnfg.read()
        if channel == 1:
            cnfg_value = cnfg_value & 0x3
            cnfg_value = cnfg_value | int('0100',2)
            if irq_type == AIIRQType.RISING.value:
                cnfg_value = cnfg_value | int('1000', 2)
        else:
            cnfg_value = cnfg_value & 0xc
            cnfg_value = cnfg_value | int('0001', 2)
            if irq_type == AIIRQType.RISING.value:
                cnfg_value = cnfg_value | int('0010', 2)
        cnfg.write(cnfg_value)

        self.callback_function = callback_function
        self.timeout = timeout
        self.irq_number = irq_number

    def wait(self):
        """
        Configure AIIRQ and execute the interrupt events.
        """
        self.acknowledge(self.irq_number)
        self.irq_wait(self.timeout, self.irq_number)

    def close(self):
        """ Close AI IRQ session"""
        self.ai.close()
        super(AIIRQ, self).close()


class TimerIRQ(IRQ):
    """
    NI ELVIS III TimerIRQ API.
    """
    def __init__(self, callback_function, irq_interval):
        """
        Initialize TimerIRQ registration.

        Args:
            callback_function (function):
                Specifies the reference to a callback function.
            irq_interval (int):
                Specify the span of time, in milliseconds, between two
                adjacent interrupts.
        """
        super(TimerIRQ, self).__init__()
        assert callable(callback_function), "callback_function need to be a function"
        assert irq_interval > 0
        self.write = self.session.registers['IRQ.TIMER.WRITE']
        self.set = self.session.registers['IRQ.TIMER.SETTIME']
        self.write.write(irq_interval)
        self.set.write(True)
        self.callback_function = callback_function
        self.irq_interval = irq_interval

    def wait(self):
        """
        Configure TimerIRQ and execute the interrupt events.
        """
        irq_number = 0
        self.acknowledge(irq_number)
        timeout = self.irq_interval+500
        self.irq_wait(timeout, irq_number)


class UART(ELVISIII):
    """
    NI ELVIS III Universal Asynchronous Receiver/Transmitter (UART) API.
    """
    def __init__(self,
                 bank=Bank.A,
                 baud_rate=UARTBaudRate.RATE9600,
                 data_bits=UARTDataBits.BITS8,
                 stop_bits=UARTStopBits.ONE,
                 parity=UARTParity.NO,
                 flow_control=UARTFlowControl.NONE):
        """
        Opens the session to one or more Universal Asynchronous
        Receiver/Transmitter (UART) channels and initialize UART registration
        on NI ELVIS III.

        Args:
            bank(Bank):
                Specifies the name of the bank to open a session. The VISA
                resource name is defined based on name of the bank. When bank
                A is selected, resource name is 'ASRL1::INSTR'. Otherwise is
                'ASRL2::INSTR'. The default value is A.
            baud_rate (UARTBaudRate):
                Specifies the rate of transmission. The default value is
                RATE9600.
            data_bits (UARTDataBits):
                Specifies the number of bits in the incoming data. The value
                of data bits is seven and eight. The default value is BITS8.
            stop_bits (UARTStopBits):
                Specifies the number of stop bits used to indicate the end of
                a frame. The default value is ONE.
            parity (UARTParity):
                Specifies the parity used for every frame to be transmitted or
                received. The default value is NO.
        """
        super(UART, self).__init__()
        assert bank in Bank
        assert baud_rate in {110, 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400}
        assert UARTDataBits.BITS7 <= data_bits <= UARTDataBits.BITS8
        assert stop_bits in UARTStopBits
        assert parity in UARTParity
        assert flow_control in UARTFlowControl
        if bank == Bank.A:
            resource_name = 'ASRL1::INSTR'
        else :
            resource_name = 'ASRL2::INSTR'
        self.a_ena = self.session.registers['UART.A.ENA']
        self.a_stat = self.session.registers['UART.A.STAT']
        self.b_ena = self.session.registers['UART.B.ENA']
        self.b_stat = self.session.registers['UART.B.STAT']
        self.console_ena = self.session.registers['CONSOLE.ENA']

        self.console_ena.write(False)
        self.a_ena.write(False)
        self.b_ena.write(False)
        if bank == Bank.A:
            while not self.a_ena.read():
                self.a_ena.write(True)
        else:
            while not self.b_ena.read():
                self.b_ena.write(True)

        self.resource_manager = pyvisa.ResourceManager()
        self.instrument = self.resource_manager.open_resource(resource_name)
        self.instrument.baud_rate = baud_rate.value
        self.instrument.data_bits = data_bits.value
        self.instrument.stop_bits = stop_bits.value
        self.instrument.parity = parity.value
        self.instrument.flow_control = flow_control.value

    def write(self, value_to_write):
        """
        Writes the data from write buffer to the device or interface specified
        by VISA resource name.

        Args:
            value_to_write (string):
                Specifies the data to be written to the device
        """
        self.instrument.write_raw(value_to_write)

    def read(self, bytes_to_read):
        """
        Reads the specified number of bytes from the device or interface
        specified by VISA resource name and returns the data in read buffer.

        Args:
            bytes_to_read (int):
                Specifies the number of bytes to be read.

        Returns:
            return_value(int):
                Returns the number of characters that function reads from the
                UART device.
        """
        assert bytes_to_read > 0 and type(bytes_to_read) == int
        return_value = ''
        while not return_value:
            return_value = self.instrument.read_bytes(bytes_to_read)
        return return_value

    def close(self):
        """
        Close UART VISA (self.instrument) and UART session (self.session).
        """
        self.instrument.close()
        super(UART, self).close()


class Button(ELVISIII):
    """ NI ELVIS III Button API. """
    def __init__(self):
        """ Initialize Button registration on NI ELVIS III. """
        super(Button, self).__init__()
        self.user_button = self.session.registers['DI.BTN']

    def read(self):
        """
        Read the result back.

        Returns:
            Current state of the LED.
        """
        return self.user_button.read() > 0


def calculate_clock_settings(requested_frequency,
                             clock_divisors,
                             max_frequency=40000,
                             min_frequency=40,
                             base_clock_frequency=40000000,
                             max_counter=65535,
                             min_counter=100,
                             coerce_range=True,
                             phase_correct_mode=False):
    """
    Determine the counter settings that will produce the requested frequency
    or as close a frequency as possible. This function is used internally and
    should only used for SPI and PWM API. Do not use this function in other
    examples.

    Args:
        requested_frequency (int):
            The range is from 40Hz to 400000Hz.
        clock_divisors (int array):
            The available clock divisors for SPI mode are 1, 2, 4, and 8. The
            available clock divisors for PWM mode are 1, 2, 4, 8, 16, 32, and
            64.
        max_frequency (int):
            The the default value is 4000000Hz.
        min_frequency (int):
            The default value is 40Hz.
        base_clock_frequency (int):
            The minmum posslbie clock frequency is 611Hz and the maximum
            possible clock frequency is 40MHz due to the impelementation in
            the FPGA. The default value is 4000000Hz.
        max_counter (int):
            NI ELVIS III is using a 16-bit counter, so the valid max counter
            value is 2^16 -1 which is equal to 65535. The default value is
            65535 which is also the suggestted value.
        min_counter (int):
            We want to guarantee 1% duty cycle resolution, the value used for
            Resolution is % x 100 is 100. The default value is 100  which is
            also the suggestted value.
        coerce_range (bool):
            The default value is True.
        phase_correct_mode (bool):
            The default value is False. The phase_correct_mode should be True
            for SPI mode; it should be False for PWM mode. 

    Returns:
        actual_frequency (float)
        actual_top (float)
        actual_clock_divisor (int)
    """
    if coerce_range:
        if not (min_frequency < requested_frequency < max_frequency):
            raise ValueError('frequency is out of range: 40 - 4000000 (Hz)')
        requested_frequency = max(min_frequency, min(requested_frequency, max_frequency))
    if requested_frequency < 0:
        requested_frequency = 0
    actual_frequency = 0
    actual_top = 0
    actual_clock_divisor = 0
    pwm_requested_frequency = requested_frequency
    for divisor in clock_divisors:
        if phase_correct_mode:
            top = round(base_clock_frequency/(2*divisor*requested_frequency))
            frequency = base_clock_frequency/(2*divisor*top)
        else:
            top = round(base_clock_frequency/(divisor*pwm_requested_frequency)) - 1
            frequency = base_clock_frequency/((top + 1)*divisor)
            min_counter -= 1
        requested_frequency = max(min_counter, min(top, max_counter))
        coerced = frequency != requested_frequency
        if coerced:
            frequency_comparison = abs(requested_frequency - actual_frequency) <= abs(requested_frequency - frequency)
            if not (frequency_comparison and (actual_frequency != 0)):
                actual_frequency = frequency
                actual_top = top
                actual_clock_divisor = divisor
        else:
            actual_frequency = frequency
            actual_top = top
            actual_clock_divisor = divisor
        if (top < min_counter) or not coerced:
            break
    return actual_frequency, actual_top, actual_clock_divisor
