import time
import sys
sys.path.append('source/nielvisiii')
from academicIO import SysSelect

sys_select = SysSelect()

channel = 3
number_of_channels_to_write = 2

result = sys_select._clear_sys_select(0xAAAAAAAA, channel, number_of_channels_to_write)
if (result != 0b10101010101010101010100000101010):
    print "clear sys select error (32bit channel 3 0xAAAAAAAA)"
result = sys_select._set_sys_select(result, channel, number_of_channels_to_write, '01')
if (result != 0b10101010101010101010100101101010):
    print "set sys select error (32bit channel 3 0xAAAAAAAA)"

result = sys_select._clear_sys_select(0xFFFFFFFF, channel, number_of_channels_to_write)
if (result != 0b11111111111111111111110000111111):
    print "clear sys select error (32bit channel 3)"
result = sys_select._set_sys_select(result, channel, number_of_channels_to_write, '01')
if (result != 0b11111111111111111111110101111111):
    print "set sys select error (32bit channel 3)"

result = sys_select._clear_sys_select(0xFFFFFFFFFFFFFFFF, channel, number_of_channels_to_write)
if (result != 0b1111111111111111111111111111111111111111111111111111110000111111):
    print "clear sys select error (64bit channel 3)"
result = sys_select._set_sys_select(result, channel, number_of_channels_to_write, '01')
if (result != 0b1111111111111111111111111111111111111111111111111111110101111111):
    print "set sys select error (64bit channel 3)"

channel = 16
number_of_channels_to_write = 3

result = sys_select._clear_sys_select(0xFFFFFFFFFFFFFFFF, channel, number_of_channels_to_write)
if (result != 0b1111111111111111111111111100000011111111111111111111111111111111):
    print "clear sys select error (64bit channel 16)"
result = sys_select._set_sys_select(result, channel, number_of_channels_to_write, '10')
if (result != 0b1111111111111111111111111110101011111111111111111111111111111111):
    print "set sys select error (64bit channel 16)"
