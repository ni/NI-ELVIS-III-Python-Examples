"""
Hardware setup:
  1. Connect DIO2 and DIO9 on connector A.
  2. Connect DIO3 and DIO10 on connector A.
  1. Connect DIO4 and DIO11 on connector A.
  2. Connect DIO8 and DIO12 on connector A.
"""
import time
# import pytest
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

bank = Bank.A
with academicIO.DigitalInputOutput(bank,
                                   [DIOChannel.DIO2, DIOChannel.DIO3, DIOChannel.DIO4, DIOChannel.DIO8,
                                    DIOChannel.DIO9, DIOChannel.DIO10, DIOChannel.DIO11, DIOChannel.DIO12]) as DIO:
    value = True

    # multiple channels
    DIO.write(value, [DIOChannel.DIO2, DIOChannel.DIO3, DIOChannel.DIO4, DIOChannel.DIO8])
    data = DIO.read([DIOChannel.DIO9, DIOChannel.DIO10, DIOChannel.DIO11, DIOChannel.DIO12])
    print data
    assert data == [1, 1, 1, 1]

    # a single channel
    DIO.write(not value, [DIOChannel.DIO3])
    data = DIO.read([DIOChannel.DIO10])
    print data
    assert data == [0]

    # multiple channels
    DIO.write(value, [DIOChannel.DIO2, DIOChannel.DIO4])
    data = DIO.read([DIOChannel.DIO9, DIOChannel.DIO11])
    print data
    assert data == [1, 1]

    try:
        DIO.write(200, [DIOChannel.DIO1])
    except (AssertionError) as err:
        print "Caught the error - Only True or False can be written to DI."

    try:
        DIO.write(value, [20])
    except (AssertionError) as err:
        print "Caught the error - The channels available in the DIO should be 0-19."

    try:
        DIO.read([20])
    except (AssertionError) as err:
        print "Caught the error - The channels available in the DIo should be 0-19."