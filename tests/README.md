The hardware connection for Python unit tests is as following.

|API|Hardware Connection||
|:--|:--|:--|
|Analog IO|AI0 - AO0||
||AI3 - AO1||
||AI2 - 3.3V||
||AI6 - 5V||
|Digital IO|DIO2 - DIO9||
||DIO3 - DIO10||
||DIO4 - DIO11||
||DIO8 - DIO12||
|Button|N/A||
|LED|N/A||
|PWM|DIO13 (PWM13) - pin0||
|Encoder|Bank A             ADXL345|ADXL345|
||DIO18 (ENC.A9)|DIO11(ENC.A)|
||DIO19 (ENC.B9)|DIO12 (ENC.B)|
||+3.3V|+3.3V|
||Ground|Ground|
|SPI|Bank A|ADXL345|
||DIO0|DIO0|
||DIO5 (SPI.CLK)|DIO5|
||DIO6 (SPI.MISO)|DIO6|
||DIO7 (SPI.MOSI)|DIO7|
||+3.3V|+3.3V|
||Ground|Ground|
|I2C|Bank A|ADXL345|
||DIO14(I2C.SCL)|I2C.SCL|
||DIO15 (I2C.SDA)|I2C.SDA|
||+3.3V|+3.3V|
||Ground|Ground|
|UART|Bank A|FTDI232|
||DIO16 (UART.RX)|TX|
||DIO17 (UART.TX)|RX|
||Ground|Ground|
||USB connect to PC||
|AI IRQ|AI1 - channel 1 of function generator||
|DI IRQ|DIO1||
|Button IRQ|N/A||
|Timer IRQ|N/A||


Due to the hardware limitation, there are some uncovered test cases below.

|API|Uncovered test cases|
|:--|:--|
|SPI|clock_phase = 'Leading'|
||clock_polarity = 'Low'|
||data_direction = 'Least Significant Bit First'|