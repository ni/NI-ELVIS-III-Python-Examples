"""
Output: 
  LED0 turns on and then LED1, LED2, LED3,
  LED0 turns off and then LED2, LED2, LED3
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import *

with academicIO.LEDs() as LED:       
    LED.write()						        # The default values are - led: led0, value_to_set = True.
    time.sleep(1)
    LED.write(led=Led.LED1)			    # The default 'value_to_set' is True
    time.sleep(1)
    LED.write(Led.LED2, True)
    time.sleep(1)
    LED.write(Led.LED3, True)
    time.sleep(1)
    LED.write(value_to_set=False)	# the default 'led' is 'led0'
    time.sleep(1)
    LED.write(Led.LED1, False)
    time.sleep(1)
    LED.write(Led.LED2, False)
    time.sleep(1)
    LED.write(Led.LED3, False)
    time.sleep(1)