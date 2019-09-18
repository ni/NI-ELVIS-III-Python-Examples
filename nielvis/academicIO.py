import os
import logging

import time
import pyvisa
import threading
from nifpga import Session
from .enums import *

class ELVISIII(object):
    """ Register NI ELVIS III bitfile. """
    ResourceName = "RIO0"

    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bitfile/ELVIS III v2.1 FPGA.lvbitx')
        self.session = Session(path, ELVISIII.ResourceName)

    def __enter__(self):
        return self

    def close(self):
        self.session.close()

    def __exit__(self, exception_type, exception_val, trace):
        self.close()


class Analog(ELVISIII):
    def __init__(self):
        super(Analog, self).__init__()

    def calculate_sample_rate_to_ticks(self, sample_rate, minimum = 1000, maximum = 30000):
        """
        Calculate and return the actual sample rate (S/s) and count (tick/s).

        Args:
            sample_rate (number):
                The expected sample rate you input.
            minimum (number):
                The minimum sample rate.
            maximum (number):
                The maximum sample rate.
        Returns:
            count (number):
                Specifies the actual count for AI.
            actual_sample_rate (number):
                Specifies the actual sample rate for AI.
        """
        if sample_rate < minimum: sample_rate = minimum
        if sample_rate > maximum: sample_rate = maximum
        fpga_clock_rate = 40000000
        count = round(fpga_clock_rate / sample_rate)
        actual_sample_rate = fpga_clock_rate / count
        return count, actual_sample_rate


class AnalogInput(Analog):
    number_of_n_sample = { 'A': 0, 'B': 0 }
    dma = { 'A': None, 'B': None }
    is_continuous_started = { 'A': False, 'B': False }

    """ NI ELVIS III Analog Input (AI) API. """
    def __init__(self, *configuration):
        """
        Opens a session to one analog input channel or multiple analog input
        channels. Then, initialize analog input registration on NI ELVIS III.

        Args:
            *configuration (array):
                bank (Bank):
                    Specifies the name of the bank to open a session.
                channel (AIOChannel):
                    Specifies the names of the analog input channels to open a
                    session. When the mode is DIFFERENTIAL, the valid AI
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

        # define local variables which are used to track whether bank A and
        # bank B are used or opened
        a_open = False
        b_open = False

        self.ready = { 'A': None, 'B': None }
        self.cnt = { 'A': None, 'B': None }
        self.cnfg = { 'A': None, 'B': None }
        self.cntr = { 'A': None, 'B': None }
        self.stat = { 'A': None, 'B': None }
        self.is_onesample_opened = { 'A': False, 'B': False }
        self.is_nsample_opened = { 'A': False, 'B': False }
        self.dma_enabled = { 'A': None, 'B': None }
        self.dma_full = { 'A': None, 'B': None }
        self.sync = { 'A': None, 'B': None }
        self.is_continuous = { 'A': False, 'B': False }
        
        self.is_bank_A_n_sample_opened = False
        self.is_bank_B_n_sample_opened = False
        
        self.__max_samples = 10000

        def __set_registration_addresses(bank):
            # get registration addresses
            self.cnfg[bank] = self.session.registers['AI.%s.CNFG' % bank]
            self.ready[bank] = self.session.registers['AI.%s.VAL.RDY' % bank]
            self.cnt[bank] = self.session.registers['AI.%s.CNT' % bank]
            self.cntr[bank] = self.session.registers['AI.%s.CNTR' % bank]
            self.stat[bank] = self.session.registers['AI.%s.STAT' % bank]

            self.dma_enabled[bank] = self.session.registers['AI.%s.DMA_ENA' % bank]

            # continous
            self.dma_full[bank] = self.session.registers['AI.%s.DMA_FULL' % bank]
            self.sync[bank] = self.session.registers['%s.SYNC' % bank]

        configuration_list = { 'A': [], 'B': [] }

        # initialize and store all channels within *configuration
        for configuration_details in configuration:
            # check whether the bank that the user configured is correct
            assert 'bank' in configuration_details
            assert 'channel' in configuration_details
            assert configuration_details['bank'] in Bank

            # set default values for mode
            if 'mode' not in configuration_details:
                configuration_details['mode'] = AIMode.SINGLE_ENDED

            # check whether the channel that the user configured is correct
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
                bank = Bank.A.value

                # get registration addresses
                __set_registration_addresses(bank)

                self.is_onesample_opened[bank] = True
                a_open = True

            # get the bank B registration addresses and initialize them
            if configuration_details['bank'] == Bank.B.value and not b_open:
                bank = Bank.B.value

                # get registration addresses
                __set_registration_addresses(bank)

                self.is_onesample_opened[bank] = True
                b_open = True

            configuration['bank'] = configuration_details['bank']
            configuration['channel'] = configuration_details['channel']
            configuration['mode'] = configuration_details['mode']
            
            configuration_list[configuration['bank']].append(configuration)

        def __calculate_configuration_values(configuration_settings):
            for channel in configuration_settings:
                configuration = {'bank': channel['bank'], 'value': channel['value'], 'cnfgval': 0}
                if channel['mode']:
                    # differential mode
                    configuration['channel'] = channel['channel'] + 8
                    configuration['value'] = self.session.registers['AI.DIFF_' + channel['bank'] + '_' + str(channel['channel']) + '.VAL']
                    configuration['cnfgval'] = channel['channel'] | channel['cnfgval']
                else:
                    # single-ended mode
                    configuration['channel'] = channel['channel']
                    configuration['value'] = self.session.registers['AI.' + channel['bank'] + '_' + str(channel['channel']) + '.VAL']
                    configuration['cnfgval'] = int(bin(channel['channel']), 2) | int('1000', 2) | channel['cnfgval']
                self.channel_list.append(configuration)
        
        self.channel_list = []
        __calculate_configuration_values(configuration_list[Bank.A.value])
        __calculate_configuration_values(configuration_list[Bank.B.value])

    def read(self, *args):
        """
        Reads values from one or more analog input channels. Use the read()
        function to read a single point of data back from the channel. Use the
        read(number_of_samples, sample_rate) function to read multiple points
        of data from the channel.

        Args:
            If you want to read a single point of data at one time, do not
            pass any arguments.
            If you want to read multiple points (n samples) of data at one
            time, arguments should contain:
                number_of_samples (number): 
                    Specifies the number of samples to read. Valid values are
                    between 0 and 10,000. 
                sample_rate (number):
                    Specifies the sampling frequency, in hertz, of the input
                    signal.
            If you want to read multiple points (continuous) of data at one
            time, arguments should contain:
                number_of_samples (number): 
                    Specifies the number of samples to read. Valid values must
                    be greater than 0. 
                timeout (number):
                    Specifies the period of time, in milliseconds, to wait for
                    the acquisition to complete. If you set Timeout to -1,
                    this function waits indefinitely. An error occurs if
                    acquisition time is longer than timeout. 

        Returns:
            return_value (array):
                Returns the value that this function reads from the analog
                input channel that you select.
        """
        args_len = len(args)
        if args_len == 0:
            return self.__read_single_point()
        elif args_len == 2:
            if self.is_continuous['A'] or self.is_continuous['B']:
                return self.__read_multiple_points_continuous(args[0], args[1])
            else:
                return self.__read_multiple_points_n_samples(args[0], args[1])
        else:
            raise TypeError('read() takes either 0 (single point) or 2 (multiple points) arguments, but given %d' % args_len)

    def start_continuous_mode(self, sample_rate):
        """
        Configure the sample rate and start the acquisition. 

        Args:
            sample_rate (number):
                Specifies the sampling frequency, in hertz, of the input
                signal. 
                If you select only one channel, the valid range for sample
                rate is between 1 Hz and 1 MHz. 
                If you select multiple channels, the valid range for sample
                rate is between 1 Hz and 250 kHz. 
        """
        number_of_channels = len(self.channel_list)

        if number_of_channels == 1:
            assert 1 <= sample_rate <= 1000000, 'If you select only 1 channel, the valid range for sample rate is between 1 Hz and 1 MHz.'
        else:
            assert 1 <= sample_rate <= 250000, 'If you select multiple channels, then the valid range for sample rate is between 1 Hz and 250 kHz.'

        self.__sample_rate = sample_rate

        def __open_ai_continuous(configuration):
            for bank in Bank:
                bank = bank.value
                if configuration[bank]['numberOfChannels'] > 0:
                    assert not AnalogInput.is_continuous_started[bank], 'Cannot open the reference to channels on one bank using more than one open function at the same time to perform continuous signal acquisition.'
                    self.__register_and_configure_dma(bank)
                    self.__stop_continuous(bank)
                    self.is_continuous[bank] = True

        def __start_ai_continuous(configuration):
            count, actual_sample_rate = self.calculate_sample_rate_to_ticks(sample_rate * number_of_channels)

            def __continuous_config_bank(bank):
                self.cnt[bank].write(0)
                self.cnfg[bank].write(configuration[bank]['cnfg'])
                self.cntr[bank].write(count)
                self.dma_enabled[bank].write(True)

                while not(self.cnt[bank].read() == 0 and self.cnfg[bank].read() == configuration[bank]['cnfg'] and self.cntr[bank].read() == count and self.dma_enabled[bank].read() == True):
                    pass

            def __reset_buffer(bank_to_reset):
                AnalogInput.dma[bank_to_reset].start()
                AnalogInput.dma[bank_to_reset].stop()

            def __check_register_values_and_enable_continuous(bank):
                while not(self.dma_enabled[bank].read() == True and self.cnt[bank].read() == configuration[bank]['numberOfChannels']):
                    pass

                AnalogInput.is_continuous_started[bank] = True

            if self.is_continuous[Bank.A.value] and self.is_continuous[Bank.B.value]:
                __continuous_config_bank(Bank.A.value)
                __continuous_config_bank(Bank.B.value)

                self.sync[Bank.A.value].write(True)
                self.sync[Bank.B.value].write(True)

                __reset_buffer(Bank.A.value)
                __reset_buffer(Bank.B.value)

                numberOfChannels = max(configuration[Bank.A.value]['numberOfChannels'], configuration[Bank.B.value]['numberOfChannels'])
                self.cnt[Bank.A.value].write(numberOfChannels)
                self.cnt[Bank.B.value].write(numberOfChannels)

                self.dma_enabled[Bank.A.value].write(True)
                self.dma_enabled[Bank.B.value].write(True)
            
                __check_register_values_and_enable_continuous(Bank.A.value)
                __check_register_values_and_enable_continuous(Bank.B.value)

                self.session.registers['SYNC'].write(True)
            else:
                bank = Bank.A.value if self.is_continuous[Bank.A.value] else Bank.B.value
                __continuous_config_bank(bank)
                __reset_buffer(bank)
                self.dma_enabled[bank].write(True)
                self.cnt[bank].write(configuration[bank]['numberOfChannels'])

                __check_register_values_and_enable_continuous(bank)

        configuration = self.__calculate_multiple_points_cnfg_and_number_of_enabled_channels()
        __open_ai_continuous(configuration)
        __start_ai_continuous(configuration)

    def __stop_continuous(self, bank):
        """
        Reset the FPGA target.

        bank (Bank):
            Specifies the name of the bank to open a session.
        """
        self.cnt[bank].write(0)
        self.dma_enabled[bank].write(False)

        while not(self.stat[bank].read() == 0):
            pass

    def stop_continuous_mode(self):
        """
        Stops signal acquisition on the FPGA target.
        """
        def __reset_continuous_registers(bank):
            self.is_continuous[bank] = False
            AnalogInput.is_continuous_started[bank] = False
            AnalogInput.dma[bank] = None
            self.__stop_continuous(bank)

        for bank in Bank:
            bank = bank.value
            if self.is_continuous[bank]:
                __reset_continuous_registers(bank)

    def __read_single_point(self):
        """
        Reads values from AI channels in AI channel list and popluates the
        output array (values) with the result. (1 sample)

        Returns:
            return_value (array):
                Returns the value, in volts, that this function reads from the
                analog input channel that you select.
        """
        current_cnfg = { 'A': None, 'B': None }
        is_opened  = { 'A': None, 'B': None }
        a_current_cnfg = ""
        b_current_cnfg = ""
        a_opened = False
        b_opened = False

        def __initialize_bank_configuration(bank):
            if self.is_onesample_opened[bank]:
                # congifure the AI channels to read
                self.cnfg[bank].write([8,9,10,11,12,13,14,15,0,1,2,3])
                # regsiter the number of valid channels
                self.cnt[bank].write(12)
                # register the analog sample rate
                # 1000 = 40 MHz FPGA Clock Frequency / 40 KHz (desired rate)
                # thus 1000 indicates a sample rate of 40 KHz here
                self.cntr[bank].write(1000)

        def __get_cnfgval(bank, cnfgval):
            current_cnfg = self.cnfg[bank].read()
            current_cnfg[channel['channel']] = cnfgval
            return current_cnfg

        def __write_to_cnfg_register(bank, cnfg):
            self.cnfg[bank].write(cnfg)
            while not(cnfg == self.cnfg[bank].read() and self.ready[bank].read()):
                pass

            # after the configuration is modified, wait 500 us before applying
            # the AI registers. 12*1000/40 M = 300 us < 500 us
            time.sleep(0.5)

        for bank in Bank:
            __initialize_bank_configuration(bank.value)

        # set the current configuration for all channels within channel_list
        for channel in self.channel_list:
            bank = channel['bank']
            current_cnfg[bank] = __get_cnfgval(bank, channel['cnfgval'])
            is_opened[bank] = True

        for bank_name in is_opened:
            if is_opened[bank_name]:
                __write_to_cnfg_register(bank_name, current_cnfg[bank_name])

        # append all the read back values and return the array
        return_value = []
        for channellist_details in self.channel_list:
            return_value.append(float(channellist_details['value'].read()))
        return return_value

    def __calculate_multiple_points_cnfg_and_number_of_enabled_channels(self):
        bank_A = {'cnfg': [0 for i in range(12)], 'numberOfChannels': 0}
        bank_B = {'cnfg': [0 for i in range(12)], 'numberOfChannels': 0}

        for channel in self.channel_list:
            if channel['bank'] == Bank.A.value:
                bank_A['cnfg'][bank_A['numberOfChannels']] = channel['cnfgval']
                bank_A['numberOfChannels'] += 1
            else:
                bank_B['cnfg'][bank_B['numberOfChannels']] = channel['cnfgval']
                bank_B['numberOfChannels'] += 1

        return {'A': bank_A, 'B': bank_B}

    def __register_and_configure_dma(self, bank):
        if AnalogInput.dma[bank] is None:
                AnalogInput.dma[bank] = self.session.fifos['AI.%s.DMA' % bank]
                AnalogInput.dma[bank].configure(self.__max_samples * 100)

    def __read_multiple_points_n_samples(self, number_of_samples, sample_rate):
        """
        Reads values from AI channels in AI channel list and popluates the
        output array (values) with the result. (n samples)

        Args:
            number_of_samples (number): 
                Specifies the number of samples to read. Valid values are
                between 0 and 10,000. 
            sample_rate (number):
                Specifies the sampling frequency, in hertz, of the input
                signal. 
                If you select only one channel, the valid range for sample
                rate is between 1 Hz and 1 MHz. 
                If you select multiple channels, the valid range for sample
                rate is between 1 Hz and 500 KHz. 
        Returns:
            return_value (array):
                Returns the values, in volts, that this function reads from
                the analog input channel that you select. The structure of the
                returned values is [ [bank_A_values], [bank_B_values] ].
        """
        number_of_channels = len(self.channel_list)
        if number_of_channels == 1:
            assert 1 <= sample_rate <= 1000000, 'If you select only 1 channel, then the valid range for sample rate is between 1 Hz and 1 MHz.'
        else:
            assert 1 <= sample_rate <= 500000, 'If you select multiple channels, then the valid range for sample rate is between 1 Hz and 500 kHz.'
        assert 0 <= number_of_samples <= self.__max_samples

        configuration = self.__calculate_multiple_points_cnfg_and_number_of_enabled_channels()

        count, actual_sample_rate = self.calculate_sample_rate_to_ticks(sample_rate * number_of_channels)

        return_value = []

        def __read_values_if_has_enabled_channels(bank):
            if configuration[bank]['numberOfChannels'] > 0:
                return_value.append(self.__read_multiple_points_n_samples_from_specific_bank(bank, configuration[bank]['cnfg'], configuration[bank]['numberOfChannels'], number_of_samples, count))

        __read_values_if_has_enabled_channels(Bank.A.value)
        __read_values_if_has_enabled_channels(Bank.B.value)

        return return_value

    def __read_multiple_points_n_samples_from_specific_bank(self, bank, configuration, number_of_channels, number_of_samples, count):
        """
        Reads values from analog channels specified in the configuration using
        the DMA. (n samples)

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session.
            configuration (Object): 
                Specifies the configuration for selected channels.
            number_of_channels (number):
                Specifies the number of channels to read.
            number_of_samples (number): 
                Specifies the number of samples to read. Valid values are
                between 0 and 10,000. 
            count (number):
                Specifies the actual count for AI.
            max_samples (number):
                Specifies the maximum number of samples for the AI n samples.

        Returns:
            return_value (array):
                Returns the values, in volts, that this function reads from the
                analog input channel that you select. The structure of the
                returned values is [ [first_channel_values],
                [second_channel_values], ...].
        """
        self.__register_and_configure_dma(bank)

        if not self.is_nsample_opened[bank]:
            self.is_nsample_opened[bank] = True
            AnalogInput.number_of_n_sample[bank] += 1

        self.cnt[bank].write(0)
        self.cnfg[bank].write(configuration)
        self.cntr[bank].write(count)
        self.dma_enabled[bank].write(True)
        ## make sure the following registers are set correcrly: cnt, cnfg, cntr, dma_enabled
        while not(self.cnt[bank].read() == 0 and self.cnfg[bank].read() == configuration and self.cntr[bank].read() == count and self.dma_enabled[bank].read() == True):
            pass

        AnalogInput.dma[bank].start()
        AnalogInput.dma[bank].stop()

        self.cnt[bank].write(number_of_channels)
        while not(self.cnt[bank].read() == number_of_channels):
            pass

        max_readback_samples = self.__max_samples
        number_of_expected_samples = number_of_channels * number_of_samples
        readvalue = []
        while number_of_expected_samples > max_readback_samples:
            readvalue.extend(AnalogInput.dma[bank].read(max_readback_samples, timeout_ms=-1)[0])
            number_of_expected_samples = number_of_expected_samples - max_readback_samples
        readvalue.extend(AnalogInput.dma[bank].read(number_of_expected_samples, timeout_ms=-1)[0])

        self.dma_enabled[bank].write(False)

        self.cnt[bank].write(0)
        while not(self.stat[bank].read() == 0):
            pass

        result = []
        for index in range(0, number_of_channels):
            result.append(readvalue[index::number_of_channels])
        return result

    def __read_multiple_points_continuous(self, number_of_samples, timeout):
        """
        Read values from AI channels in AI channel list and populate the
        output array (values) with the result. (continuous)

        Args:
            number_of_samples (number): 
                Specifies the number of samples to read. Valid values must be
                greater than 0. 
            timeout (number):
                Specifies the period of time, in milliseconds, to wait for the
                acquisition to complete. If you set Timeout to -1, this
                function waits indefinitely. An error occurs if acquisition
                time is longer than timeout. 
        Returns:
            return_value (array):
                Returns the values, in volts, that this function reads from
                the analog input channel that you select. 
                The value is returned in the following format: [ [bank_A_values], [bank_B_values] ].
        """
        assert 0 <= number_of_samples
        if timeout != -1:
            assert timeout >= (number_of_samples / self.__sample_rate)

        def __read_from_specific_bank(bank, number_of_channels):
            assert self.cnt[bank].read() == number_of_channels, 'The continuous acquisition has not started. You must call the start_continuous_mode() function before calling the read() function.'
            assert not self.dma_full[bank].read(), 'The read buffer has overflowed. This error occurs when you do not call the read() function after the acquisition starts for a while. You must call the read() function before the buffer overflows. This error may also occur when you set a high sample rate, for example, 1 MHz. In this case, you can modify the number of samples to a value between 3,000 and 50,000 to fit the buffer size.'

            read_timeout = timeout
            max_readback_samples = self.__max_samples
            number_of_expected_samples = number_of_channels * number_of_samples
            readvalue = []

            while number_of_expected_samples > max_readback_samples:
                time_to_start_reading = time.time()
                readvalue.extend(AnalogInput.dma[bank].read(max_readback_samples, timeout_ms=read_timeout)[0])
                time_taken_to_read_once = time.time() - time_to_start_reading
                number_of_expected_samples = number_of_expected_samples - max_readback_samples

                if read_timeout != -1:
                    read_timeout = 0 if read_timeout - time_taken_to_read_once < 0 else read_timeout - time_taken_to_read_once

            readvalue.extend(AnalogInput.dma[bank].read(number_of_expected_samples, timeout_ms=read_timeout)[0])

            result = []
            for index in range(0, number_of_channels):
                result.append(readvalue[index::number_of_channels])
            return result

        return_value = []

        def __read_values_if_has_enabled_channels(bank, number_of_channel_per_bank):
            if self.is_continuous[bank]:
                return_value.append(__read_from_specific_bank(bank, number_of_channel_per_bank[bank]))
        
        def __get_number_of_channel_per_bank():
            number_of_channel_per_bank = {'A': 0, 'B':0}
            for channel in self.channel_list:
                number_of_channel_per_bank[channel['bank']] += 1
            return number_of_channel_per_bank

        number_of_channel_per_bank =__get_number_of_channel_per_bank()
        __read_values_if_has_enabled_channels(Bank.A.value, number_of_channel_per_bank)
        __read_values_if_has_enabled_channels(Bank.B.value, number_of_channel_per_bank)

        return return_value
    
    def _toBinary(self, num):
        return bin(int(num))

    def close(self):
        def __update_number_of_opened_n_sample(bank):
            if self.is_nsample_opened[bank]:
                AnalogInput.number_of_n_sample[bank] -= 1

        def __clear_dma_reference(bank):
            if AnalogInput.number_of_n_sample[bank] == 0:
                AnalogInput.dma[bank] = None

        self.stop_continuous_mode()

        for bank in Bank:
            __update_number_of_opened_n_sample(bank.value)
            __clear_dma_reference(bank.value)

        super(AnalogInput, self).close()


class AnalogOutput(Analog):
    dma = { 'A': None, 'B': None }
    number_of_n_sample = { 'A': 0, 'B': 0 }
    
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
        self.dma_idl = { 'A': None, 'B': None }
        self.dma_cntr = { 'A': None, 'B': None }
        self.dma_ena = { 'A': None, 'B': None }
        self.is_nsample_opened = { 'A': False, 'B': False }

        self.channel_list = []
        for configuration_details in configuration:
            assert 'bank' in configuration_details
            assert 'channel' in configuration_details
            assert configuration_details['bank'] in Bank
            assert AOChannel.AO0 <= configuration_details['channel'] <= AOChannel.AO1

            configuration_details['bank'] = configuration_details['bank'].value
            configuration_details['channel'] = configuration_details['channel'].value
            configuration_details['value_address'] = self.session.registers['AO.' + configuration_details['bank'] + '_' + str(configuration_details['channel']) + '.VAL']
            self.enamask = configuration_details['channel']^2
            self.channel_list.append(configuration_details)

        for bank in Bank:
            self.dma_idl[bank.value] = self.session.registers['AO.%s.DMA_IDL' % bank.value]
            self.dma_cntr[bank.value] = self.session.registers['AO.%s.DMA_CNTR' % bank.value]
            self.dma_ena[bank.value] = self.session.registers['AO.%s.DMA_ENA' % bank.value]
            
        self.dma_sys_ready = self.session.registers['DMA.SYS.RDY']
        self.go = self.session.registers['AO.SYS.GO']
        self.stat = self.session.registers['AO.SYS.STAT']
        self.lsb_weights = 4882813.0 / 1E+9
        self.offset = 0.0 / 1E+9
        self.signed = True

    def write(self, *args):
        """
        Writes values to one or more analog output channels. Use the
        write(value) function to write a single point of data to the channel. Use
        the write(values, sample_rate) to write multiple points of data to the
        channel. The function hangs until the write to physical I/O
        operation completes.

        Args:
            If you want to write a single point of data at one time, argument
            should contain:
                value (number):
                    Specifies the value, in volts, to write to the analog output
                    channels. The value must be in the range of +/-10. If you
                    specify a value that is invalid, this function coerces the
                    specified value to the nearest valid value when you execute
                    the program.
            If you want to write multiple points of data at one time, arguments
            should contain:
                values (list):
                    Specifies the values, in volts, to write to the analog output
                    channels. Values is a 2D array. The number of elements in each
                    row represents the number of samples to write to each analog
                    output channel. Ensure this number is greater than 0 and less
                    than or equal to 10,000.
                sample_rate (number):
                    Specifies the sampling frequency, in hertz, of the output signal.
        """
        args_len = len(args)
        if args_len == 1:
            self.__write_single_point(args[0])
        elif args_len == 2:
            self.__write_multiple_points(args[0], args[1])
        else:
            raise TypeError('write() takes either 1 (single point) or 2 (multiple points) arguments, but given %d' % args_len)

    def __write_single_point(self, value):
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
        assert type(value) == int or type(value) == float
        for channel in self.channel_list:
            bank = channel['bank']
            self.dma_ena[bank].write(0)
            while not(self.dma_ena[bank].read() == 0):
                pass

            stat_value = not self.stat.read()
            self.value = channel['value_address']
            self.value.write(value)
            self.go.write(True)
            while not(self.stat.read() == stat_value):
                pass
    
    def __write_multiple_points(self, values, sample_rate):
        """
        Writes values to one or more analog output channels. (n samples)

        Args:
            values (list):
                Specifies the values, in volts, to write to the analog output
                channels. Values is a 2D array. The number of elements in each
                row represents the number of samples to write to each analog
                output channel. Ensure this number is greater than 0 and less
                than or equal to 10,000.
            sample_rate (number):
                Specifies the sampling frequency, in hertz, of the output
                signal.
        """
        minimum_sample_rate = 1000
        maximum_sample_rate = 1600000
        minimum_samples = 1
        maximum_samples = 10000
        assert type(values) == list
        assert all(type(value) == int or type(value) == float for value in values)
        assert type(sample_rate) == int or type(sample_rate) == float
        assert minimum_sample_rate <= sample_rate <= maximum_sample_rate

        def __calculate_bitmask():
            bitmask_array = [[False, False] for i in range(2)]
            for channel in self.channel_list:
                first_index = 0 if channel['bank'] == Bank.A.value else 1
                second_index = 0 if channel['channel'] == AOChannel.AO0.value else 1
                bitmask_array[first_index][second_index] = True

            bitmask_in_int = []
            for bitmask_for_bank in bitmask_array:
                bitmask_for_channel = int('10', 2) if bitmask_for_bank[1] == True else int('00', 2)
                bitmask_for_channel = (bitmask_for_channel | int('01', 2)) if bitmask_for_bank[0] == True else bitmask_for_channel
                bitmask_in_int.append(bitmask_for_channel)

            return bitmask_in_int

        for channel in self.channel_list:
            bank = channel['bank']
            if not self.is_nsample_opened[bank]:
                self.is_nsample_opened[bank] = True
                AnalogOutput.number_of_n_sample[bank] += 1
            if AnalogOutput.dma[bank] is None:
                AnalogOutput.dma[bank] = self.session.fifos['AO.%s.DMA' % bank]
                AnalogOutput.dma[bank].configure(maximum_samples * 20)

        bitmask = __calculate_bitmask()

        count, actual_sample_rate = self.calculate_sample_rate_to_ticks(sample_rate, minimum_sample_rate, maximum_sample_rate)
        
        data = [ int(value * int('1000000000000000000000000000', 2)) for value in values ]

        while not(self.dma_sys_ready.read() == True):
            pass

        if self.is_nsample_opened[Bank.A.value]:
            self.__write_multiple_points_to_specific_bank(Bank.A.value, count, data, bitmask[0])
        if self.is_nsample_opened[Bank.B.value]:
            self.__write_multiple_points_to_specific_bank(Bank.B.value, count, data, bitmask[1])

    def __write_multiple_points_to_specific_bank(self, bank, count, data, channel_bitmask):
        """
        Writes output values to the specified AO channel on the FPGA.

        Args:
            bank (Bank):
                Specifies the name of the bank, on which to open a session.
            count (number):
                Specifies the actual count for AO.
            data (list):
                Specifies the values, in volts, to write to the analog output
                channels.
            channel_bitmask (number):
                Specifies the channel. AO0 is 2 and AO1 is 1 for n samples.
        """
        def __write(bank, count, data, channel_bitmask):

            def __write_and_return_remaining_data(data_to_write, max_write_samples):
                AnalogOutput.dma[bank].write(data_to_write[:max_write_samples], timeout_ms=0)
                return data_to_write[max_write_samples:]

            self.dma_ena[bank].write(channel_bitmask)
            self.dma_cntr[bank].write(count)
            while not(self.dma_cntr[bank].read() == count):
                pass
            
            data_length = len(data)
            max_write_samples = 10000

            if data_length <= max_write_samples:
                AnalogOutput.dma[bank].write(data, timeout_ms=0)
            else:
                data = __write_and_return_remaining_data(data, max_write_samples)
                max_write_samples = 5000

                while len(data) != 0:
                    empty_elements_remaining = AnalogOutput.dma[bank].write([], timeout_ms=0)
                    
                    if empty_elements_remaining > max_write_samples:
                        data = __write_and_return_remaining_data(data, max_write_samples)
                    else:
                        AnalogOutput.dma[bank].write(data, timeout_ms=0)
                        data = []

        def __wait_until_write_done(bank):
            """
            Configure IRQ, execute it, and wait until it is asserted, which
            means the write to physical I/O operation completes. The irq
            number is 31 for Bank A and 30 for Bank B.
            """
            irq_number = { 'A': 31, 'B': 30 }
            irq_status = self.session.wait_on_irqs(irq_number[bank], -1)
            self.session.acknowledge_irqs(irq_status.irqs_asserted)
            self.dma_ena[bank].write(0)

        irq_thread = threading.Thread(target=__write,
                                      args=(bank, count, data, channel_bitmask))
        irq_thread.start()
        __wait_until_write_done(bank)
        irq_thread.join()

    def close(self):
        def __update_number_of_opened_n_sample(bank):
            if self.is_nsample_opened[bank]:
                AnalogOutput.number_of_n_sample[bank] -= 1

        def __clear_dma_reference(bank):
            if AnalogOutput.number_of_n_sample[bank] == 0:
                AnalogOutput.dma[bank] = None

        for bank in Bank:
            __update_number_of_opened_n_sample(bank.value)
            __clear_dma_reference(bank.value)

        super(AnalogOutput, self).close()

class SysSelect(ELVISIII):
    def __init__(self):
        super(SysSelect, self).__init__()

    def clear_sys_select(self, register_value, start_channel, number_of_channels_to_write):
        """
        Clear the system select register for DIO, PWM, Encoder, SPI, and I2C.
        Args:
            register_value
            start_channel (int): 
                The start channel of the channels to write to.
            number_of_channels_to_write: 
                Number of channels to write to. DIO and PWM are one; Encoder and
                I2C are two. SPI is three.
        """
        for i in range(number_of_channels_to_write):
            register_value &= ~(int('11', 2) << ((start_channel + i) * 2))
        return register_value

    def set_sys_select(self, register_value, start_channel, number_of_channels_to_write, bits_to_write):
        """
        Set the system select register for DIO, PWM, Encoder, SPI, and I2C.
        Args:
            register_value
            start_channel (int): 
                The start channel of the channels to write to.
            number_of_channels_to_write (int): 
                Number of channels to write to. DIO and PWM are one; Encoder and
                I2C are two. SPI is three.
            bits_to_write (string):
                Specify a 2 bits data to write to the channels as shows in the
                following:
                    DIO             '00'
                    PWM             '01'
                    Encoder         '11'
                    SPI and I2C     '11'
        """
        for i in range(number_of_channels_to_write):
            register_value = register_value | (int(bits_to_write, 2) << ((start_channel + i) * 2))
        return register_value

class DigitalInputOutput(SysSelect):
    """ NI ELVIS III Digital Input and Output (DIO) API. """
    def __init__(self, bank=Bank.A, channels=[]):
        """
        Opens a session to one or more digital input and output channels.
        Then, initialize digital I/O registration on NI ELVIS III.

        Args:
            bank (Bank):
                Specifies the name of the bank to open a session. The default
                value is A.
            channel (array):
                Specifies the names of the digital I/O channels.
        """
        super(DigitalInputOutput, self).__init__()
        assert bank in Bank
        assert channels
        bank = bank.value
        self.write_registration = self.session.registers['DIO.' + bank + '_19:0.OUT']
        self.read_registration = self.session.registers['DIO.' + bank + '_19:0.IN']
        self.direction = self.session.registers['DIO.' + bank + '_19:0.DIR']
        self.select = self.session.registers['SYS.SELECT' + bank]
        self.direction.write(0x00)

        for channel in channels:
            assert DIOChannel.DIO0 <= channel <= DIOChannel.DIO19
            system_select_value = self.clear_sys_select(self.select.read(), channel, 1)
            self.select.write(system_select_value)
        self.channels = channels

    def read(self, channels_to_read=[]):
        """
        Reads the logic levels of one or more digital I/O channels. (1 sample)

        Args:
            *channels_to_read (DIOChannel):
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
        for channel in channels_to_read:
            assert channel in self.channels
            return_value.append(int(0 < (int(value) & (1 << channel.value))))
        return return_value

    def write(self, value, channels_to_write=[]):
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
            *channels_to_write (DIOChannel):
                Specifies the names of the digital I/O channels to write to.
                This value can be a single channel (ex: 7) or a list of
                channels (ex: 7, 8 ,9).
        """
        assert type(value) == bool
        direction_value = int('00000000000000000000', 2)
        write_value = int('0000000000000000000', 2)  
        for channel in channels_to_write:
            assert channel in self.channels
            direction_value |= (1 << channel.value)
            write_value |= (int(value) << channel.value)
        self.direction.write(direction_value)
        self.write_registration.write(write_value)      


class Encoder(SysSelect):
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
        self.select = self.session.registers['SYS.SELECT' + bank]

        if encoder_mode == EncoderMode.QUADRATURE:
            self.cnfg.write(int('00000001', 2))
        else:
            self.cnfg.write(int('00000101', 2))

        # ENC used two DIO channels at once, therefore the channel need to *2
        # for example, ENC0 = DIO0 + DIO1
        system_select_value = self.clear_sys_select(self.select.read(), 2 * channel, 2)
        system_select_value = self.set_sys_select(system_select_value, 2 * channel, 2, '10')
        self.select.write(system_select_value)

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


class PWM(SysSelect):
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
        self.select = self.session.registers['SYS.SELECT' + bank]

        system_select_value = self.clear_sys_select(self.select.read(), channel, 1)
        system_select_value = self.set_sys_select(system_select_value, channel, 1, '01')
        self.select.write(system_select_value)

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
        assert 40 <= frequency <= 400000
        assert 0 <= duty_cycle <= 1
        clock_divisors = [1, 2, 4, 8, 16, 32, 64]
        actual_frequency, top, clock_divisor = calculate_clock_settings(frequency, clock_divisors, False)
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


class I2C(SysSelect):
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
        self.select = self.session.registers['SYS.SELECT' + bank]
        self.cntr = self.session.registers['I2C.' + bank + '.CNTR']
        self.cnfg = self.session.registers['I2C.' + bank + '.CNFG']
        self.addr = self.session.registers['I2C.' + bank + '.ADDR']
        self.cntl = self.session.registers['I2C.' + bank + '.CNTL']
        self.dato = self.session.registers['I2C.' + bank + '.DATO']
        self.go = self.session.registers['I2C.' + bank + '.GO']
        self.stat = self.session.registers['I2C.' + bank + '.STAT']
        self.dati = self.session.registers['I2C.' + bank + '.DATI']
        self.configure(mode)

        system_select_value = self.set_sys_select(self.select.read(), 14, 2, '11')
        self.select.write(system_select_value)

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
        assert len(bytes_to_write) >= 0
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


class SPI(SysSelect):
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
        bank = bank.value
        clock_phase = clock_phase.value
        clock_polarity = clock_polarity.value
        data_direction = data_direction.value
        self.select = self.session.registers['SYS.SELECT' + bank]
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
        actual_frequency, top, clock_divisor = calculate_clock_settings(frequency, clock_divisors, False, 4000000, 40, 20000000,
                                                                        65535, 1, True)
        index = 0
        for clock_number in clock_divisors:
            if clock_number == clock_divisor:
                break
            index += 1
        spi_cnfg = spi_cnfg | (index << 14)
        self.cnfg.write(spi_cnfg & 0xFFFF)
        self.cnt.write(int(top) & 0xFFFF)

        system_select_value = self.set_sys_select(self.select.read(), 5, 3, '11')
        self.select.write(system_select_value)

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
        logging.getLogger().setLevel(logging.INFO)
        logging.info('waiting for IRQ...')
        irq_status = self.session.wait_on_irqs([irq_number], timeout)
        if irq_number in irq_status.irqs_asserted:
            message = str(irq_number) + " was asserted. IRQ occured."
            logging.info(message)
            self.callback_function()
            self.acknowledge(irq_number)
        else:
            message = str(irq_number), "was not asserted. Timeout."
            logging.info(message)

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
        assert type(irq_number) == IRQNumber
        assert IRQNumber.IRQ1 <= irq_number <= IRQNumber.IRQ8
        assert type(timeout) == int
        assert timeout >= 0
        assert type(threshold) == float or type(threshold) == int
        assert 0 <= threshold <= 5
        assert type(hysteresis) == float or type(threshold) == int
        assert 0 <= hysteresis <= 1
        assert irq_type == AIIRQType.RISING or irq_type == AIIRQType.FALLING

        self.ai = AnalogInput({'bank': Bank.A, 'channel': channel})
        self.ai.read()

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
                             phase_correct_mode,
                             max_frequency=40000,
                             min_frequency=40,
                             base_clock_frequency=40000000,
                             max_counter=65535,
                             min_counter=100,
                             coerce_range=True):
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
        phase_correct_mode (bool):
            The phase_correct_mode should be False for SPI mode; it should be
            True for PWM mode. 
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
    for divisor in clock_divisors:
        if phase_correct_mode:
            top = round(base_clock_frequency / (2 * divisor * requested_frequency))
            frequency = base_clock_frequency / (2 * top * divisor)
        else:
            top = round(base_clock_frequency / (divisor * requested_frequency)) - 1
            frequency = base_clock_frequency / (divisor * (1 + top))
            min_counter -= 1
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
