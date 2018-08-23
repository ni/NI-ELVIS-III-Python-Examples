# Table of Contents
 - [Introduction](#introduction)
 - [Register Naming Convention](#register-naming-convention)
   * [Peripheral Type](#peripheral-type)
   * [Channel Name](#channel-name)
   * [Property Names](#property-names)
 - [System Control / Function Select](#system-control--function-select)
   * [Function Select Registers (SYS.SELECTx)](#function-select-registers-sysselectx)
 - [Onboard Device Registers](#onboard-device-registers)
   * [LEDs (DIO.LED)](#leds-dioled)
   * [Button (DI.BTN)](#button-dibtn)
 - [AI/AO](#aiao)
   * [Analog Counter Register (AI.x.CNT)](#analog-counter-register-aixcnt)
   * [Analog Configuration Registers (AI.x.CNFG)](#analog-configuration-registers-aixcnfg)
   * [Analog Divisor Registers (AI.x.CNTR, AO.x.DMA_CNTR)](#analog-divisor-registers-aixcntr-aoxdma\_cntr)
   * [Analog Input DMA Enable Registers (AI.x.DMA_ENA)](#analog-input-dma-enable-registers-aixdma\_ena)
   * [Analog Output DMA Enable Registers (AO.x.DMA_ENA)](#analog-output-dma-enable-registers-aoxdma\_ena)
   * [Analog DMA IDLE Registers (AI.x.DMA_IDL, AO.x.DMA_IDL)](#analog-dma-idle-registers-aixdma\_idl-aoxdma\_idl)
   * [Analog Value Registers (AI.x.VAL, AO.x.VAL)](#analog-value-registers-aixval-aoxval)
   * [Analog Output Set Register (AO.SYS.GO)](#analog-output-set-register-aosysgo)
   * [Analog Output Status Register (AO.SYS.STAT)](#analog-output-status-register-aosysstat)
 - [DIO](#dio)
   * [Data Direction Registers (DIO.x.DIR)](#data-direction-registers-dioxdir)
   * [Pin Input Registers (DIO.x.IN)](#pin-input-registers-dioxin)
   * [Pin Output Registers (DIO.x.OUT)](#pin-output-registers-dioxout)
   * [Digital Divisor Registers (DI.x.DMA_CNTR, DO.x.DMA_CNTR)](#digital-divisor-registers-dixdma\_cntr-doxdma\_cntr)
   * [Digital Input DMA Enable Registers (DI.x.DMA_ENA)](#digital-input-dma-enable-registers-dixdma\_ena)
   * [Digital Output DMA Enable Registers (DO.x.DMA_ENA)](#digital-output-dma-enable-registers-doxdma\_ena)
   * [Digital DMA IDLE Registers (DI.x.DMA_IDL, DO.x.DMA_IDL)](#digital-dma-idle-registers-dixdma\_idl-doxdma\_idl)
 - [PWM](#pwm)
   * [PWM Configuration Registers (PWM.x.CNFG)](#pwm-configuration-registers-pwmxcnfg)
   * [PWM Clock Select Registers (PWM.x.CS)](#pwm-clock-select-registers-pwmxcs)
   * [PWM Maximum Count Registers (PWM.x.MAX)](#pwm-maximum-count-registers-pwmxmax)
   * [PWM Compare Registers (PWM.x.CMP)](#pwm-compare-registers-pwmxcmp)
   * [PWM Counter Registers (PWM.x.CNTR)](#pwm-counter-registers-pwmxcntr)
   * [PWM Frequency Generation](#pwm-frequency-generation)
 - [SPI Master](#spi-master)
   * [SPI Configuration Registers (SPI.x.CNFG)](#spi-configuration-registers-spixcnfg)
   * [SPI Counter Registers (SPI.x.CNT)](#spi-counter-registers-spixcnt)
   * [SPI Execute Registers (SPI.x.GO)](#spi-execute-registers-spixgo)
   * [SPI Status Registers (SPI.x.STAT)](#spi-status-registers-spixstat)
   * [SPI Data Out Registers (SPI.x.DATO)](#spi-data-out-registers-spixdato)
   * [SPI Data In Registers (SPI.x.DATI)](#spi-data-in-registers-spixdati)
   * [SPI Frequency Generation](#spi-frequency-generation)
 - [Encoder](#encoder)
   * [Encoder Configuration Registers (ENC.x.CNFG)](#encoder-configuration-registers-encxcnfg)
   * [Encoder Status Registers (ENC.x.STAT)](#encoder-status-registers-encxstat)
   * [Encoder Counter Value Registers (ENC.x.CNTR)](#encoder-counter-value-registers-encxcntr)
 - [I2C](#i2c)
   * [I2C Configuration Registers (I2C.x.CNFG)](#i2c-configuration-registers-i2cxcnfg)
   * [I2C Slave Address Registers (I2C.x.ADDR)](#i2c-slave-address-registers-i2cxaddr)
   * [I2C Counter Registers (I2C.x.CNTR)](#i2c-counter-registers-i2cxcntr)
   * [I2C Data Out Registers (I2C.x.DATO)](#i2c-data-out-registers-i2cxdato)
   * [I2C Data In Registers (I2C.x.DATI)](#i2c-data-in-registers-i2cxdati)
   * [I2C Status Registers (I2C.x.STAT)](#i2c-status-registers-i2cxstat)
   * [I2C Control Registers (I2C.x.CNTL)](#i2c-control-registers-i2cxcntl)
   * [I2C Execute Registers (I2C.x.GO)](#i2c-execute-registers-i2cxgo)
   * [I2C Sequence Flowcharts](#i2c-sequence-flowcharts)
     + [Sending a Single Byte](#sending-a-single-byte)
     + [Receiving a Single Byte](#receiving-a-single-byte)
     + [Sending Multiple Bytes](#sending-multiple-bytes)
     + [Receiving Multiple Bytes](#receiving-multiple-bytes)
     + [Sending Multiple Bytes then Receiving Multiple Bytes](#sending-multiple-bytes-then-receiving-multiple-bytes)
     + [Receiving Multiple Bytes then Sending Multiple Bytes](#receiving-multiple-bytes-then-sending-multiple-bytes)
 - [UART](#uart)
   * [UART Enable Register (UART.x.ENA)](#uart-enable-register-uartxena)
   * [UART Status Register (UART.x.STAT)](#uart-status-register-uartxstat)
 + [IRQ](#irq)
   * [Timer Interrupt](#timer-interrupt)
     + [Timer Read Register (IRQ.TIMER.READ)](#timer-read-register-irqtimerread)
     + [Timer Write Register (IRQ.TIMER.WRITE)](#timer-write-register-irqtimerwrite)
     + [Timer Set Time Register (IRQ.TIMER.SETTIME)](#timer-set-time-register-irqtimersettime)
   * [Analog Input Interrupt](#analog-input-interrupt)
     + [Analog IRQ Threshold Register (IRQ.AI_x.THRESHOLD)](#analog-irq-threshold-register-irqai\_xthreshold)
     + [Analog IRQ Hysteresis Register (IRQ.AI_x.HYSTERESIS)](#analog-irq-hysteresis-register-irqai\_xhysteresis)
     + [Analog IRQ Configuration Register (IRQ.AI_x.CNFG)](#analog-irq-configuration-register-irqai\_xcnfg)
     + [Analog IRQ Number Register (IRQ.AI_x.NO)](#analog-irq-number-register-irqai\_xno)
   * [Digital Input Interrupt](#digital-input-interrupt)
     + [Digital Enabling Register (IRQ.DIO_x.ENA)](#digital-enabling-register-irqdio\_xena)
     + [Digital Rising Register (IRQ.DIO_x.RISE)](#digital-rising-register-irqdio\_xrise)
     + [Digital Falling Register (IRQ.DIO_x.FALL)](#digital-falling-register-irqdio\_xfall)
     + [Digital IRQ Number Register (IRQ.DIO_x.NO)](#digital-irq-number-register-irqdio\_xno)
     + [Digital Count Register (IRQ.DIO_A_0.CNT)](#digital-count-register-irqdio\_a\_0cnt)
   * [Button Interrupt](#button-interrupt)
     + [Button Enabling Register (IRQ.DI_BTN.ENA)](#button-enabling-register-irqdi\_btnena)
     + [Button Rising Register (IRQ.DI_BTN.RISE)](#button-rising-register-irqdi\_btnrise)
     + [Button Falling Register (IRQ.DI_BTN.FALL)](#button-falling-register-irqdi\_btnfall)
     + [Button IRQ Number Register (IRQ.DI_BTN.NO)](#button-irq-number-register-irqdi\_btnno)
     + [Button Count Register (IRQ.DI_BTN.CNT)](#button-count-register-irqdi\_btncnt)


# NI ELVIS III Shipping Personality Reference

This document contains reference information about the NI ELVIS III shipping personality which consists of predefined FPGA bitfile for you to program with NI ELVIS III. 

## Introduction 

The LabVIEW ELVIS III Toolkit will also ship an FPGA personality as default, and it provides support for the following peripherals:

- Onboard devices (LEDs, button)
- Analog input
- Analog output
- Digital input/output
- Pulse-width modulation (PWM)
- Serial peripheral interface (SPI)
- Encoder
- Inter-integrated circuit (I2C)
- Universal asynchronous receiver-transmitter (UART)
- Interrupt request (IRQ)

Each peripheral is controlled through the use of its corresponding registers as outlined in this document.

## Register Naming Convention

Registers follow a naming scheme as described below:

```
Peripheral Type.Channel Name.Property Name
```

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 


### Peripheral Type

Possible values = {AI, AO, DIO, DI, DO, PWM, I2C, SPI, ENC, IRQ, SYS}

| Short Name  | Full Name                                   | 
|-------------|---------------------------------------------| 
| AI          | Analog input                                | 
| AO          | Analog output                               | 
| DIO         | Digital input/output                        | 
| DI          | Digital input                               | 
| DO          | Digital output                              | 
| PWM         | Pulse-width modulation                      | 
| I2C         | Inter-integrated circuit                    | 
| SPI         | Serial peripheral interface                 | 
| ENC         | Encoder                                     | 
| UART        |	Universal asynchronous receiver-transmitter |
| IRQ         | Interrupt request                           | 
| SYS         | System                                      | 


> Note: SYS is a reserved value used for a special purpose system register. The system
registers may or may not be related to a specific peripheral.

### Channel Name

The Channel Name is a combination of the bank designation and its numeric enumeration or range enumeration. An underscore (_) separates the channels bank designation and its enumeration. The enumeration is omitted if only one channel of that type is available on the bank. 

Example: A_7:0 indicates that the register corresponds to channels 0 to 7 on Bank A.

### Property Names

The following tables list all possible property names. Some properties are only applicable
to a single peripheral while others may be used across multiple peripherals.

<p align="center">
Table 1. Inputs (controls)
</p>

| Short Name  | Long Name      | Comment                                                                                                                                            | 
|-------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------| 
| DIR         | Direction      | Controls the direction of the DIO pins.                                                                                                            | 
| OUT         | Output         | The value of the signal to be set at the DIO output pins.                                                                                          | 
| CNFG        | Configuration  | Used to configure a peripheral. Usually used to indicate some setting that does not change after initialization or at least changes infrequently.  | 
| CNTL        | Control        | Used to control a peripheral. Usually used for control bits that are used often at run time, such as start or clear bits.                          | 
| CMP         | Compare        | The compare value. Used by peripherals that compare one value to another value.                                                                    | 
| MAX         | Maximum        | The maximum value for some internal counter.                                                                                                       | 
| CS          | Clock Select   | The desired clock to be used.                                                                                                                      | 
| ADDR        | Address        | The address to be used.                                                                                                                            | 
| DATO        | Data Out       | The data to be sent to an attached device.                                                                                                         | 
| CNT         | Count          | The count value to be used by an internal counter. Usually used to control the rate of operation of a subsystem or signal generation.              | 
| GO          | Go             | Used to start an operation on a peripheral.                                                                                                        | 
| VAL         | Value          | The value written to a subsystem/onboard device. Also used as an output.                                                                           | 


<p align="center">
Table 2. Outputs (indicators)
</p>

| Short Name  | Long Name   | Comment                                                                 | 
|-------------|-------------|-------------------------------------------------------------------------| 
| IN          | Input       | The value currently present at the DIO input lines.                     | 
| STAT        | Status      | The status of a peripheral.                                             | 
| CNTR        | Counter     | The value of some counter.                                              | 
| DATI        | Data In     | The data received from an attached device.                              | 
| VAL         | Value       | The value read from a subsystem/onboard device. Also used as an input.  | 
| WGHT        | Weight      | The scaling weight to convert to/from physical units.                   | 
| OFST        | Offset      | The offset from zero.                                                   | 
| READ        | Read        | The remaining time before the FPGA timer elapses.                       | 
| WRITE       | Write       | The elapse time to be set to the FPGA timer.                            | 
| SETTIME     | Set Time    | The toggle to overwrite the elapse time in the FPGA timer.              | 
| ENA         | Enable      | Enables the setting of a peripheral.                                    | 
| RISE        | Rise        | Enables the rising edge interrupt.                                      | 
| FALL        | Fall        | Enables the falling edge interrupt.                                     | 
| NO          | Number      | The identifier of the interrupt.                                        | 
| THRESHOLD   | Threshold   | The value that triggers the analog input interrupts.                    | 
| HYSTERESIS  | Hysteresis  | The window size for threshold to reduce noise.                          |

## System Control / Function Select

### Function Select Registers (SYS.SELECTx)

The function select registers control the functionality that is routed to the shared pins. You must enable the desired functionality at run time by setting or clearing the appropriate bits before you use the individual registers. The bit definition of each register for each bank type is given below. 

> Tip: Changing the register value switches between functions. This may have undesired effects if the connected peripheral is not intended to be connected to the alternate function.

Register list: SYS.SELECTA, SYS.SELECTB

Data type: U64

SYS.SELECTA and SYS.SELECTB select functionality on banks A DIO [0:19] and B DIO [0:19], respectively. In this register, each DIO is represented by 2 bits from low to high. For example, Bits [0:1] is DIO 0, Bits [2:3] is DIO 1, etc. The functionality of the combination of 2 bits is shown in the following table: 

| Bits  | Functionality                      | 
|-------|------------------------------------| 
| 00    | The channel is used as DIO.        | 
| 01    | The channel is used as PWM.        | 
| 10    | The channel is used as Encoder.    | 
| 11    | The channel is used as SPI or I2C. | 

For each DIO channel on banks A and B, it could have different functionalities: 

- DIO: DIO [0:19] on banks A and B 
- PWM: DIO [0:19] on banks A and B 
- Encoder: DIO [0:1], DIO [2:3], …, DIO [18:19] on banks A and B 
- SPI: DIO [5:7] on banks A and B 
- I2C: DIO [14:15] on banks A and B 

| DIO     | PWM     | Encoder  | SPI       | I2C      | UART     | 
|---------|---------|----------|-----------|----------|----------| 
| DIO 0   | PWM 0   | ENC.A 0  |           |          |          | 
| DIO 1   | PWM 1   | ENC.B 0  |           |          |          | 
| DIO 2   | PWM 2   | ENC.A 1  |           |          |          | 
| DIO 3   | PWM 3   | ENC.B 1  |           |          |          | 
| DIO 4   | PWM 4   | ENC.A 2  |           |          |          | 
| DIO 5   | PWM 5   | ENC.B 2  | SPI.CLK   |          |          | 
| DIO 6   | PWM 6   | ENC.A 3  | SPI.MISO  |          |          | 
| DIO 7   | PWM 7   | ENC.B 3  | SPI.MOSI  |          |          | 
| DIO 8   | PWM 8   | ENC.A 4  |           |          |          | 
| DIO 9   | PWM 9   | ENC.B 4  |           |          |          | 
| DIO 10  | PWM 10  | ENC.A 5  |           |          |          | 
| DIO 11  | PWM 11  | ENC.B 5  |           |          |          | 
| DIO 12  | PWM 12  | ENC.A 6  |           |          |          | 
| DIO 13  | PWM 13  | ENC.B 6  |           |          |          | 
| DIO 14  | PWM 14  | ENC.A 7  |           | I2C.SCL  |          | 
| DIO 15  | PWM 15  | ENC.B 7  |           | I2C.SDA  |          | 
| DIO 16  | PWM 16  | ENC.A 8  |           |          | UART.RX  | 
| DIO 17  | PWM 17  | ENC.B 8  |           |          | UART.TX  | 
| DIO 18  | PWM 18  | ENC.A 9  |           |          |          | 
| DIO 19  | PWM 19  | ENC.B 9  |           |          |          | 

## Onboard Device Registers

These registers control the onboard LEDs and read the onboard button and accelerometer.

### LEDs (DIO.LED)

Register list: DIO.LED3:

Data type: U8

| Bit            | 7  | 6  | 5  | 4  | 3     | 2     | 1     | 0     | 
|----------------|----|----|----|----|-------|-------|-------|-------| 
| Name           | -  | -  | -  | -  | LED3  | LED2  | LED1  | LED0  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0     | 0     | 0     | 0     | 

This register controls the state of the onboard LEDs. Each bit corresponds to a single LED. If the bit is set to 1, the LED is lit. If the bit is set to 0, the LED is unlit.

- Bits [7:4] - Reserved for future use.
- Bits [3:0] - LED3:

The desired state of onboard LEDs 3 to 0.

### Button (DI.BTN)

Register list: DI.BTN

Data type: U8

| Bit            | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0      | 
|----------------|----|----|----|----|----|----|----|--------| 
| Name           | -  | -  | -  | -  | -  | -  | -  | BTN    | 
| Initial Value  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0 or 1 | 

This register indicates the current state of the onboard button. A value of 1 means the button is pressed. A value of 0 means the button is not pressed. The button is internally debounced so you don’t need to add additional debouncing logic in software.

- Bits [7:1] - Reserved for future use.
- Bit [0] - BTN

The state of the onboard button. The initial value is either 0 or 1, depending on the initial state of this button.

## AI/AO

There are 8 analog input channels for each bank (A/B), and they support single-ended measurement which measures the difference between the selected signal and AI Ground and differential measurement which measures the difference between the selected signal and its associated signal pair. The following table shows the channel mapping for each mode.

| Bank    |Application Board Terminals|Single-ended Mode|Differential Mode| 
|---------|--------|--------|---------| 
| Bank A  | A/AI0  | AI 0   | AI 0 +  | 
|         | A/AI1  | AI 1   | AI 1 +  | 
|         | A/AI2  | AI 2   | AI 2 +  | 
|         | A/AI3  | AI 3   | AI 3 +  | 
|         | A/AI4  | AI 4   | AI 0 -  | 
|         | A/AI5  | AI 5   | AI 1 -  | 
|         | A/AI6  | AI 6   | AI 2 -  | 
|         | A/AI7  | AI 7   | AI 3 -  | 
| Bank B  | B/AI0  | AI 0   | AI 0 +  | 
|         | B/AI1  | AI 1   | AI 1 +  | 
|         | B/AI2  | AI 2   | AI 2 +  | 
|         | B/AI3  | AI 3   | AI 3 +  | 
|         | B/AI4  | AI 4   | AI 0 -  | 
|         | B/AI5  | AI 5   | AI 1 -  | 
|         | B/AI6  | AI 6   | AI 2 -  | 
|         | B/AI7  | AI 7   | AI 3 -  | 

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 

### Analog Counter Register (AI.x.CNT)

Register list: AI.A.CNT, AI.B.CNT

Data type: U8

This register shows how many valid channels there are in AI.X.CNFG and AI.X.VAL.

### Analog Configuration Registers (AI.x.CNFG)

Register list: AI.A.CNFG, AI.B.CNFG

Data type: Array of U

This register configures the AI channels to read. The number of the elements in the array
depends on the AI.X.CNT register. The value of the configuration is shown in the
following table.

| Bit            | 7           | 6  | 5                  | 4                     | 3  | 2  | 1  | 0  | 
|----------------|-------------|----|--------------------|-----------------------|----|----|----|----| 
| Name           | First Tick  | -  | AI Range   | AI Range  |  AI Mode  |  AI Channel Selection  |  AI Channel Selection  | AI Channel Selection   | 
| Initial Value  | 0           | 0  | 0                  | 0                     | 0  | 0  |  0  |  0  |

- Bit 7: First Tick Flag. True means this is the first tick after updating the configuration, and the data of this tick should be acquired.  
- Bit 6: Reserved for future use. 
- Bits [5:4]: Specify the voltage range of the analog input channel 
    o ±10 V: 00b
    o 	±5 V: 01b
    o 	±2 V: 10b
    o 	±1 V: 11b 
- Bit 3: Specify the acquisition mode of the analog input channel  
    o DIFF: 0
    o 	RSE: 1 
- Bits [2:0]: Specify which AI channel to configure.  
    o Channel 0: 000b
    o Channel 1: 001b
    o ...
    o Channel 7: 111b

### Analog Divisor Registers (AI.x.CNTR, AO.x.DMA_CNTR)

Register list: AI.A.CNTR, AI.B.CNTR, AO.A.DMA_CNTR, AO.B.DMA_CNTR

Data type: U32

This register is the divisor for the analog sample rate. The default onboard clock rate of FPGA is 40 MHz. This register equals the default onboard clock divided by the expected sample rate.

### Analog Input DMA Enable Registers (AI.x.DMA_ENA)

Register list: AI.A.DMA_ENA, AI.A.DMA_ENA

Data type: Boolean

Each eight analog input channels share one DMA on bank A and B respectively. This register controls whether the DMA is enabled for a specific bank. 

### Analog Output DMA Enable Registers (AO.x.DMA_ENA)

Register list: AI.A.DMA_ENA, AI.A.DMA_ENA

Data type: FXP

Each two analog output channels share one DMA on bank A and B respectively. This register controls whether the DMA is enabled for a specific analog output

| Bit           | 1   | 0   | 
|---------------|-----|-----| 
| Name          | AO1 | AO0 | 
| Initial Value | 0   | 0   | 

### Analog DMA IDLE Registers (AI.x.DMA_IDL, AO.x.DMA_IDL)

Register list: AI.A.CNT, AI.B.CNT

Data type: Boolean

This register shows whether the DMA is idle.

### Analog Value Registers (AI.x.VAL, AO.x.VAL)

Analog Input

Register list: AI.A_[0:7].VAL, AI.DIFF_A_[0:3] .VAL, AI.B_[0:7].VAL,
AI.DIFF_B_[0:3].VAL

Data type: FXP

This register contains the value read by the analog input channel, and depends on
AI.X.CNFG. These registers should be used only in one sampling acquisition. For N
sampling, you should use the DMA directly.

Analog Output

Register list: AO.A_0.VAL, AO.A_1.VAL, AO.B_0.VAL, AO.B_1.VAL

Data type: FXP

This register contains the value written from the analog output channel. These registers
should be used only in one sampling acquisition. For N sampling, you should use the
DMA directly.

### Analog Output Set Register (AO.SYS.GO)

Register list: AO.SYS.GO

Data type: Boolean

This register causes values written to the AO.x.VAL registers to take effect. Values
written to the Analog Output VAL registers don’t take effect until the AO.SYS.GO bit is
strobed. You only need to write TRUE to this register as the register resets to FALSE after
the write operation starts and the output is maintained until this register is again set to
TRUE. Values for all registers are set for a single strobe of the GO register. Care should
be taken to not change a VAL register if you do not want the output voltage to change
when GO is strobed.

### Analog Output Status Register (AO.SYS.STAT)

Register list: AO.SYS.STAT

Data type: Boolean

This register toggles every time the analog output write operation completes. If the value
is read before the GO register is toggled, it can be used to determine when the write
operation completes by waiting for the value to change from the initial value.

## DIO

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 

### Data Direction Registers (DIO.x.DIR)

Register list: DIO.A_19:0.DIR, DIO.B_19:0.DIR

Data type: FXP

This register controls the direction of the DIO channels. Each bit in the register controls
the direction of one channel in the bank. For example, bit 0 corresponds to DIO 0, and bit
19 corresponds to DIO 19.

### Pin Input Registers (DIO.x.IN)

Register list: DIO.A_19:0.IN, DIO.B_19:0.IN

Data type: FXP

This register indicates the value read on the DIO channel. Each bit in the register indicates
the value of one channel in the bank. For example, bit 0 corresponds to DIO 0, and bit 19
corresponds to DIO 19. The read value is 1 when a digital high voltage is applied to the
pin. The read value is 0 when a digital low voltage is applied to the pin. The read value of
output channels is undefined.

### Pin Output Registers (DIO.x.OUT)

Register list: DIO.A_19:0.OUT, DIO.B_19:0.OUT

Data type: FXP

This register controls the value written on the DIO channel. Each bit in the register
controls the value on one channel in the bank. For example, bit 0 corresponds to DIO 0,
and bit 19 corresponds to DIO 19. If the bit is set to 1, the pin returns a digital high
voltage. If the bit is set to 0, the pin returns a digital low voltage. Output values only take
effect when the channel is configured to be an output channel. If the OUT register is
written to but the channel is set as an input, there is no effect on the pin. However, if the
channel is changed to be an output, the voltage at the pin changes to be the value
corresponding to the last value written to the OUT register.

For example, if Channel A/DIO0 is set as an input but left unconnected and the IN register
is read, bit 0 reads a value of 1. If a 0 is written to bit 0 of the OUT register, there is no
effect on the hardware and bit 0 of the IN register is still 1. However, if the channel is
changed to an output, the value read on bit 0 of the IN register immediately changes to a 0
and a low voltage returns at the pin.

> Note: This follows the functionality of the Set Output Data and Set Output Enable
FPGA IO Method nodes. Refer to the LabVIEW Help for more information about
using FPGA I/O.

### Digital Divisor Registers (DI.x.DMA_CNTR, DO.x.DMA_CNTR)

Register list: DI.A.DMA_CNTR, DI.B.DMA_CNTR, DO.A.DMA_CNTR,
DO.B.DMA_CNTR

Data type: U16

This register is the divisor for the digital sample rate. The default onboard clock rate of
FPGA is 40 MHz. This register equals the default onboard clock divided by the expected
sample rate.

### Digital Input DMA Enable Registers (DI.x.DMA_ENA)

Register list: DI.A.DMA_ENA, DI.B.DMA_ENA

Data type: Boolean

Each twenty digital input channels share one DMA on bank A and B respectively. This register controls whether the DMA is enabled for all digital input channels on the bank. 

### Digital Output DMA Enable Registers (DO.x.DMA_ENA)

Register list: DO.A.DMA_ENA, DO.B.DMA_ENA

Data type: FXP

Each twenty digital output channels share one DMA on bank A and B respectively. This register controls whether the DMA is enabled for specific digital output channel. 

### Digital DMA IDLE Registers (DI.x.DMA_IDL, DO.x.DMA_IDL)

Register list: DI.A.DMA_IDL, DI.B.DMA_IDL, DO.A.DMA_IDL, DO.B.DMA_IDL

Data type: Boolean

This register shows whether the DMA is idle.

## PWM

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 

### PWM Configuration Registers (PWM.x.CNFG)

Register list: PWM.A_[0:19].CNFG, PWM.B_[0:19].CNFG

Data type: U8

This register configures the functionality of the PWM subsystem as shown in the
following table.

| Bit           | 7 | 6 | 5 | 4 | 3 | 2    | 1 | 0   | 
|---------------|---|---|---|---|---|------|---|-----| 
| Name          | - | - | - | - | - | MODE | - | INV | 
| Initial Value | 0 | 0 | 0 | 0 | 0 | 0    | 0 | 0   | 

- Bits [7:3] - Reserved for future use.
- Bit [2] - MODE: Counter mode.

The mode of operation of the PWM counter.

- MODE = 0:

The counter operates in no PWM generation mode. The counter counts up to 65535, resets
to 0, and repeats. The MAX and CMP registers have no effect on the counter and no PWM
output is generated.

- MODE = 1:

The counter operates in PWM generation mode. The counter counts up to the value
specified in the MAX register, resets to 0, and repeats. When the value equals the CMP
register, a compare match occurs. The behavior of the PWM output on compare match is
determined by the INV bit.

- Bit [1] - Reserved for future use.
- Bit [0] - INV : Invert Output

The functionality of this bit depends on the value of the MODE bit. When MODE = 0, the
INV bit is not used. When MODE = 1, the INV bit causes the following behavior:

- INV = 0:

Clear the output on compare match, set at min counter value (non-inverting mode).

- INV = 1:

Set the output on compare match, clear at min counter value (inverting mode).

### PWM Clock Select Registers (PWM.x.CS)

Register list: PWM.A_[0:19].CS, PWM.B_[0:19].CS

Data type: U8

This register controls the clock speed of the PWM counter.

| Bit           | 7 | 6 | 5 | 4 | 3 | 2   | 1   | 0   | 
|---------------|---|---|---|---|---|-----|-----|-----| 
| Name          | - | - | - | - | - | CS2 | CS1 | CS0 | 
| Initial Value | 0 | 0 | 0 | 0 | 0 | 0   | 0   | 0   | 

- Bits [7:3] - Reserved for future use.
- Bits [2:0] - CS : Clock select

| CS2 | CS1 | CS0 | Clock           | 
|-----|-----|-----|-----------------| 
| 0   | 0   | 0   | Off (No clock)  | 
| 0   | 0   | 1   | 1x (fclk)       | 
| 0   | 1   | 0   | 2x (fclk / 2)   | 
| 0   | 1   | 1   | 4x (fclk / 4)   | 
| 1   | 0   | 0   | 8x (fclk / 8)   | 
| 1   | 0   | 1   | 16x (fclk / 16) | 
| 1   | 1   | 0   | 32x (fclk / 32) | 
| 1   | 1   | 1   | 64x (fclk / 64) | 

The base clock frequency (fclk) is 40 MHz. Use this frequency when you calculate the
value of MAX for the desired frequency. See the frequency generation section below on
how to use the CS register.

### PWM Maximum Count Registers (PWM.x.MAX)

Register list: PWM.A_[0:19].MAX, PWM.B_[0:19].MAX

Data type: U16

This register determines the maximum value of the PWM counter. If the MODE bit in the
CNFG register is set to 1, the PWM counter counts to MAX, then resets to 0. Otherwise,
this register is ignored.

### PWM Compare Registers (PWM.x.CMP)

Register list: PWM.A_[0:19].CMP, PWM.B_[0:19].CMP

Data type: U16

This register sets the compare value, and therefore determines the duty cycle of the PWM.
The behavior depends on the value of the MODE and INV bits in the CNFG register.

| MODE | INV    | Output Behavior                                        | 
|------|--------|--------------------------------------------------------| 
| 0    | 0 or 1 | No output. CMP value is ignored.                       | 
| 1    | 0      | Clear the output when CNTR = CMP. (non-inverting mode) | 
| 1    | 1      | Set the output when CNTR = CMP. (inverting mode)       | 

### PWM Counter Registers (PWM.x.CNTR)

Register list: PWM.A_[0:19].CNTR, PWM.B_[0:19].CNTR

Data type: U16

Range: 0 to 65535

This register indicates the current value of the PWM counter. If the MODE bit in the
CNFG register is 0, the counter increments from 0 to 65535, then resets to 0 and repeats.
If the MODE bit in the CNFG register is 1, the counter increments from 0 to the value
specified in the MAX register, then resets to 0, and repeats. The counter increments at the
rate determined by the value of the CS register.

### PWM Frequency Generation

The NI ELVIS III hardware runs on a 40 MHz clock, which means the time between clock
cycles is 25 ns. The NI ELVIS III can generate slower PWM frequencies by counting and
changing the output on intervals of rising clock edges. The NI ELVIS III can generate
PWM frequencies between 40 Hz and 40 kHz. You must downsample the 40 MHz clock
to generate a slower frequency. For example, the following figure shows the generation of
20 MHz and 10 MHz clocks from a 40 MHz clock by changing the output every rising
edge or every other rising edge, respectively.

<p align="center">
    <img src="docs/resources/mdk1.png">
</p>

<p align="center">
Figure 1. Generating Slower PWM Frequencies
</p>

Slower frequencies must be exactly divisible by the clock period of 25 ns. A 25 MHz
clock cannot be generated from the 40 MHz clock; the next slowest frequency is 20 MHz.

The NI ELVIS III PWM counters are unsigned 16-bit integers with a range of 0 to 65535.
Therefore, using the 40 MHz clock, the slowest frequency is:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{25&space;ns&space;\times&space;65536}\cong610.35Hz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{25&space;ns&space;\times&space;65536}\cong610.35Hz" title="\frac{1}{25 ns \times 65536}\cong610.35Hz" /></a> 
</p>

With this method, the achievable frequency range is ~610.35 Hz to 40 MHz, where
frequencies whose period can be divided by 25 ns can actually be generated.

The NI ELVIS III hardware provides hardware clock dividers to divide reduce the main
frequency and generate even slower frequencies. The hardware clock divider is selected
by the PWM.x.CS register. With a clock divider of 2, the new slowest achievable
frequency is:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{50&space;ns\times&space;65536}\cong&space;305.17&space;Hz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{50&space;ns\times&space;65536}\cong&space;305.17&space;Hz" title="\frac{1}{50 ns\times 65536}\cong 305.17 Hz" /></a>
</p>

The following formula describes possible frequencies:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=f_{PWM}=\frac{f_{clk}}{N(X&plus;1)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{PWM}=\frac{f_{clk}}{N(X&plus;1)}" title="f_{PWM}=\frac{f_{clk}}{N(X+1)}" /></a>
</p>

where fclk is the base clock frequency, fPWM is the desired PWM frequency, N is the clock
divider being used, and X is the number of counts before changing the signal.

The value of N is determined by the value written to the PWM.x.CS register, and X is the
value written to the PWM.x.MAX register.

> Note Attempts to generate frequencies outside the range of 40 Hz to 40 kHz are not
supported.

## SPI Master

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 

### SPI Configuration Registers (SPI.x.CNFG)

Register list: SPI.A.CNFG, SPI.B.CNFG

Data type: U16

This register configures the SPI master subsystem. It determines the clock divider, frame
length, data order, clock polarity, and clock phase settings.

| Bit            | 15   | 14   | 13  | 12  | 11  | 10  | 9  | 8  | 
|----------------|------|------|-----|-----|-----|-----|----|----| 
| Name           | CS1  | CS0  | -   | -   | -   | -   | -  | -  | 
| Initial Value  | 0    | 0    | 0   | 0   | 0   | 0   | 0  | 0  | 

| Bit            | 7       | 6       | 5       | 4       | 3      | 2      | 1      | 0  | 
|----------------|---------|---------|---------|---------|--------|--------|--------|----| 
| Name           | FLE N3  | FLE N2  | FLE N1  | FLE N0  | DOR D  | CPO L  | CPH A  | -  | 
| Initial Value  | 0       | 0       | 0       | 0       | 0      | 0      | 0      | 0  | 

- Bits [15:14] - CS : Clock Select

Selects the desired clock divider to be applied to the SPI clock generator which controls
the SPI frequency. The CS bits and the CNT register are used together to determine the
speed of the SPI transmission. The possible frequencies are shown below:

| CS1  | CS0  | Clock          | 
|------|------|----------------| 
| 0    | 0    | 1x (fclk)      | 
| 0    | 1    | 2x (fclk / 2)  | 
| 1    | 0    | 4x (fclk / 4)  | 
| 1    | 1    | 8x (fclk / 8)  | 

The base clock frequency (fclk) is set at 40 MHz. You must use this frequency when
calculating the value of the CNT register. See the frequency generation section below on
how to use the CS register.

- Bits [13:8] - Reserved for future use.

These bits are reserved for future use and should never be written to. Writing a value to
these bits is unsupported.

- Bits [7:4] - FLEN : Frame Length

Sets the length, in bits, of the frame to be transmitted or received. A frame size of 4 to 16
is supported. The value to be written must be one less the desired frame length. Therefore,
for a frame size of 8 a value of 7 must be written. Values less than 3 are not supported.
FLEN = Desired Frame Length - 1

- Bit [3] - DORD: Data Order

This bit controls the order in which the bits are transmitted. When DORD is 0, the most
significant bit of the data frame is transmitted first. When DORD is 1, the least significant
bit of the data frame is transmitted first.

- Bit [2] - CPOL: Clock Polarity

This bit controls the idle state of the SPI clock. When this bit is written to one, SPI.CLK is
high when idle. When CPOL is written to zero, SPI.CLK is low when idle. The CPOL
functionality is summarized below:

| CPOL  | Leading Edge  | Trailing Edge  | 
|-------|---------------|----------------| 
| 0     | Rising        | Falling        | 
| 1     | Falling       | Rising         | 

- Bit [1] - CPHA: Clock Phase

This bit controls the functionality of the leading and trailing edges of SPI.CLK on the
SPI.SDA line. The directions of the leading and trailing edges are controlled by the value
of the CPOL bit. The CPHA functionality is summarized below.

| CPHA  | Leading Edge  | Trailing Edge  | 
|-------|---------------|----------------| 
| 0     | Sample        | Setup          | 
| 1     | Setup         | Sample         | 


- Bit [0] - Reserved for future use.

<p align="center">
    <img src="docs/resources/mdk2.png">
</p>

<p align="center">
Figure 2. SPI Transfer Format with CPHA = 0
</p>

<p align="center">
    <img src="docs/resources/mdk3.png">
</p>

<p align="center">
Figure 3. SPI Transfer Format with CPHA = 1
</p>

### SPI Counter Registers (SPI.x.CNT)

Register list: SPI.A.CNT, SPI.B.CNT

Data type: U16

This register controls the maximum value of the SPI counter. This value and the clock
divider setting in the CNFG register determine the speed of the SPI transmission. See the
frequency generation section below on how to use the CS register.

### SPI Execute Registers (SPI.x.GO)

Register list: SPI.A.GO, SPI.B.GO

Data type: Boolean

This register starts an SPI data transfer. You only need to write a TRUE value to this
register as the register resets to FALSE after the transfer starts. The data transmitted is
taken from the DATO register while the data received is placed in the DATI register.
During a transfer, the DATI register is invalid until the operation is complete, but the
value of the DATO register can be changed while a SPI transfer is in progress. When a
transfer is in progress, the value of the GO register is ignored. You must wait till the
operation is complete before setting the GO register to TRUE again. The status of the SPI
transfer can be determined using the STAT register.

### SPI Status Registers (SPI.x.STAT)

Register list: SPI.A.STAT, SPI.B.STAT

Data type: U8

The register indicates the status of the SPI subsystem.

| Bit            | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0    | 
|----------------|----|----|----|----|----|----|----|------| 
| Name           | -  | -  | -  | -  | -  | -  | -  | BSY  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0    | 

- Bits [7:1] - Reserved for future use.
- Bit [0] - BSY
If BSY is 1, the SPI subsystem is transferring a frame. If BSY is 0, the SPI subsystem is
idle.

### SPI Data Out Registers (SPI.x.DATO)

Register list: SPI.A.DATO, SPI.B.DATO

Data type: U16

This register holds the data that is sent to the slave device during the next transmission.

The FLEN bits in the SPI.x.CNTL register determines the length of the data transmitted.
Bits in the SPI.x.DATO register outside of the specified frame length are ignored. For
example, if the SPI.x.DATO register contains 65535 (0xFFFF) and the frame length is 8
bits, only the lower 8 bits are transmitted.

### SPI Data In Registers (SPI.x.DATI)

Register list: SPI.A.DATO, SPI.B.DATO

Data type: U16

This register holds the data that is received from the slave device during the last
transmission. The FLEN bits in the SPI.x.CNTL register determines the length of the data
received. The SPI subsystem only attempts to receive the number of bits specified. If the
slave device transmits 9 bits per frame but the frame length is set at 8 bits, the last bit is
ignored and the DATI register contains only the 8 bits received. On the next SPI transfer,
the slave may try to send the last bit from the previous transmission.

### SPI Frequency Generation

The NI ELVIS III hardware runs on a 40 MHz clock, which means the time between clock
cycles is 25 ns. The NI ELVIS III can generate slower SPI frequencies by counting and
changing the output on intervals of rising clock edges. The NI ELVIS III can generate SPI
frequencies between 40 Hz and 4 MHz. You must downsample the 40 MHz clock to
generate a slower frequency. For example, the following figure shows the generation of 20
MHz and 10 MHz clocks from a 40 MHz clock by changing the output every rising edge
or every other rising edge, respectively.

<p align="center">
    <img src="docs/resources/mdk4.png">
</p>

<p align="center">
Figure 4. Generating Slower SPI Frequencies
</p>

Slower frequencies must be exactly divisible by the clock period of 25 ns. A 25 MHz
clock cannot be generated from the 40 MHz clock; the next slowest frequency is 20 MHz.

The NI ELVIS III SPI counters are unsigned 16-bit integers with a range of 0 to 65535.
Therefore, using the 40 MHz clock, the slowest frequency is:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{25&space;ns&space;\times&space;65536}\cong610.35Hz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{25&space;ns&space;\times&space;65536}\cong610.35Hz" title="\frac{1}{25 ns \times 65536}\cong610.35Hz" /></a> 
</p>

Using this method, the achievable frequency range is ~610.35 Hz to 40 MHz, where
frequencies whose period can be divided by 25ns can actually be generated.

In order for generating even slower frequencies, the NI ELVIS III hardware provides a
series of clock dividers (N). The clock dividers function as described above, where the
base frequency is divided into even numbers (2, 4, 8, etc) and the generated clock is used
to increment the counter. With a clock divider of 2, and a U16 counter, the new slowest
achievable frequency is:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{50&space;ns\times&space;65536}\cong&space;305.17&space;Hz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{50&space;ns\times&space;65536}\cong&space;305.17&space;Hz" title="\frac{1}{50 ns\times 65536}\cong 305.17 Hz" /></a>
</p>

The possible SPI frequencies that can be generated are based on the following equation:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=f_{SPI}=\frac{f_{clk}}{2\times&space;N\times&space;(X&plus;1)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{SPI}=\frac{f_{clk}}{2\times&space;N\times&space;(X&plus;1)}" title="f_{SPI}=\frac{f_{clk}}{2\times N\times (X+1)}" /></a>
</p>

where fclk is the base clock frequency, fSPIis the desired SPI frequency, N is the clock
divider being used, and X is the number of counts before changing the signal.

The value of N is determined by the value written to the CS bits in the CNTL register, and
X is the value written to the CNT register.

> Note: Attempts to generate frequencies outside the range of 40 Hz to 4 MHz are not
supported.

## Encoder

The quadrature encoder block counts the number of steps that an encoder makes about its axis of rotation. The angular change per step is determined by the resolution of the encoder being used. When the encoder is going forward, the count value is incremented. When the encoder is moving backwards, the count value is decremented. There are two modes that are supported by the implemented encoder (ENC) subsystem. In the step and direction mode, the direction signal indicates the direction of rotation where a low signal means forward and a high signal means backward. The count value changes on every rising edge of the step signal. In the quadrature phase mode, the encoder generates two signals called Phase A and Phase B, which are two square waves that are 90 degrees out of phase with each other.In general, when Phase A is leading Phase B, the encoder counter is counting up, and when Phase B leads Phase A, the encoder counter is counting down. The count value is changed on every change of Phase A or Phase B. The following figure shows a waveform with the Phase A and Phase B signals and the equivalent step (clk) and direction (dir) signals. 
<p align="center">
    <img src="docs/resources/mdk5.png">
</p>

<p align="center">
Figure 5. A Waveform with Phase A, Phase B, Step (CLK), and Direction (DIR) Signals
</p>

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”). 

### Encoder Configuration Registers (ENC.x.CNFG)

Register list: ENC.A_[0:9].CNFG, ENC.B_[0:9].CNFG

Data type: U8

This register configures the encoder subsystem.

| Bit            | 7  | 6  | 5  | 4     | 3     | 2     | 1    | 0   | 
|----------------|----|----|----|-------|-------|-------|------|-----| 
| Name           | -  | -  | -  | COVR  | CERR  | MODE  | RST  | EN  | 
| Initial Value  | 0  | 0  | 0  | 0     | 0     | 0     | 0    | 0   | 

- Bits [7:5] - Reserved for future use.
- Bit [4] - COVR: Clear Overflow

Clears all the overflow related flags (UOVR, SOVR, UOERR, SOERR) in the ENC Status
Register (STAT). The flags are cleared on the rising edge on this signal, which is when the
value goes from 0 to 1. It should be manually reset to 0 after use.

- Bit [3] - CERR: Clear Error

Clears the error flag (ERR) in the ENC Status Register (STAT). The flag is cleared on the
rising edge on this signal, which is when the value goes from 0 to 1. It should be manually
reset to 0 after use.

- Bit [2] - MODE: Signal Mode

The mode of operation of the ENC block. When MODE is written with a 0, it operates in
quad phase mode. When MODE is written with a 1, it operates in step and direction mode.

- Bit [1] - RST: Reset

Resets the value of the ENC counter to 0. The counter remains at 0 as long as this bit has a
value of 1.

- Bit [0] - EN: Enable

Enables the ENC block. When it is written with 0, the ENC block is disabled and the
count value and direction flag do not change. When it is written with a 1, the block is
enabled.

### Encoder Status Registers (ENC.x.STAT)

Register list: ENC.A_[0:9].STAT, ENC.B_[0:9].STAT

Data type: U8

| Bit            | 7  | 6  | 5      | 4      | 3     | 2     | 1    | 0    | 
|----------------|----|----|--------|--------|-------|-------|------|------| 
| Name           | -  | -  | SOERR  | UOERR  | SOVR  | UOVR  | ERR  | DIR  | 
| Initial Value  | 0  | 0  | 0      | 0      | 0     | 0     | 0    | 0    | 

Configures the encoder subsystem for the desired behavior.

- Bits [7:6] - Reserved for future use.
- Bit [5] - SOERR: Signed Overflow Error

Indicates that a signed overflow error has occurred. When this bit is 1, a signed overflow
occurred while the SOVR flag is already set as 1. This indicates that a signed overflow
occurred before the SOVR flag is cleared and therefore, the state of the SOVR flag cannot
be trusted as it is not possible to know how many times overflow has occurred. This bit
remains at 1 until it is cleared by writing a 1 to the COVR bit in the CNFG register.

- Bit [4] - UOERR: Unsigned Overflow Error

Indicates that an unsigned overflow error has occurred. The bit is set to 1 when an
unsigned overflow occurs while the UOVR flag is already set as 1. This indicates that an
unsigned overflow occurred before the UOVR flag was cleared and therefore, the state of
the UOVR flag cannot be trusted as it is not possible to know how many times overflow
has occurred. This bit remains at 1 until it is cleared by writing a 1 to the COVR bit in the
CNFG register.

- Bit [3] - SOVR: Signed Overflow

Indicates that a signed overflow has occurred. The counter value is stored as an unsigned
32-bit value which can represent both a signed or unsigned number. If you want to treat
the stored value as a signed number then use this overflow flag and ignore the UOVR flag.
When this bit is 1, the counter value has gone from the maximum value (2147483647) to
the minimum value (-2147483648) or has gone from the minimum value to the maximum
value. When this bit is 0, no overflow has occurred. This bit remains at 1 until it is cleared
by writing a 1 to the COVR bit in the CNFG register.

- Bit [2] - UOVR: Unsigned Overflow

Indicates that an unsigned overflow has occurred. The counter value is stored as an
unsigned 32-bit value that can represent both a signed or unsigned number. If you want to
treat the stored value as an unsigned number, use this overflow flag and ignore the SOVR
flag. When this bit is 1, the counter value has gone from the maximum value
(4294967296) to 0 or has gone from 0 to the maximum value. When this bit is 0, no
overflow has occurred. This bit remains at 1 until it is cleared by writing a 1 to the COVR
bit in the CNFG register.

- Bit [1] - ERR: Error

Indicates that an error has occurred when operating in quad phase mode. This bit will
never be 1 while operating in step and direction mode. A value of 1 indicates that an error
occurs. This is usually caused by the values of both the Phase A and Phase B signals
changing at the same time. When this bit is 1, the counter value and direction bit do not
update based on the encoder input but hold the last valid value. This bit remains at 1 until
it is cleared by writing a 1 to the CERR bit in the CNFG register.

- Bit [0] - DIR: Direction

Indicates the last direction of the last change to the encoder counter value. A value of 0
indicates that the encoder counter was incremented while a value of 1 indicates that the
encoder counter was decremented.

### Encoder Counter Value Registers (ENC.x.CNTR)

Register list: ENC.A_[0:9].CNTR, ENC.B_[0:9].CNTR

Data type: U32

Unsigned range: 0 to 4294967296

Signed range: -2147483648 to 2147483647

The number of steps that the encoder has gone through based on the value of the MODE
bit in CNFG. In quad phase mode, the counter value increments when the Phase A leads
Phase B and decrements when Phase B leads Phase A. In step and direction mode, the
counter increments when the direction input is low and decrements when the direction
input is high. Both signed and unsigned numbers are stored as unsigned 32-bit values so if

the user wants to treat the value as a signed number they must convert it before they use
the value.

## I2C

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”).

### I2C Configuration Registers (I2C.x.CNFG)

Register list: I2C.A.CNFG, I2C.B.CNFG

Data type: U8

This register enables or disables the I2C subsystem.

| Bit            | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0       | 
|----------------|----|----|----|----|----|----|----|---------| 
| Name           | -  | -  | -  | -  | -  | -  | -  | MSTREN  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 0       | 

- Bits [7:1] - Reserved for future use.
- Bit [0] - MSTREN: Enable or disable I2C functionality.

### I2C Slave Address Registers (I2C.x.ADDR)

Register list: I2C.A.ADDR, I2C.B.ADDR

Data type: U8

This register sets the address and transmission direction of the slave device.

| Bit            | 7    | 6    | 5    | 4    | 3    | 2    | 1    | 0    | 
|----------------|------|------|------|------|------|------|------|------| 
| Name           | SA6  | SA5  | SA4  | SA3  | SA2  | SA1  | SA0  | R/S  | 
| Initial Value  | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 

- Bits [7:1] - SA : Slave address

Specifies the 7-bit address for the slave device that is being communicated with.

- Bit [0] - R/S : Receive/send

Specifies if the next transmission operation to be completed is a send or receive
operation.

- 0: Send
- 1: Receive

### I2C Counter Registers (I2C.x.CNTR)

Register list: I2C.A.CNTR, I2C.B.CNTR

Data type: U8

Specifies the counter value the I2C subsystem must use to generate the clock during a
send or receive operation.

The value of the CNTR register can be calculated using the following equation:

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=f_{SCL}=\frac{f_{clk}}{(2\times&space;CNTR)-26}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{SCL}=\frac{f_{clk}}{(2\times&space;CNTR)-26}" title="f_{SCL}=\frac{f_{clk}}{(2\times CNTR)-26}" /></a>
</p>

where fSCL is the desired I2C transmission frequency and fclk is the base clock frequency
of the hardware (40 MHz).

For example, for a standard-mode transmission of 100 kbps:

fSCL= 100 kHz

fclk = 40 MHz

Since 
<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=f_{SCL}=\frac{f_{clk}}{(2\times&space;CNTR)-26}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{SCL}=\frac{f_{clk}}{(2\times&space;CNTR)-26}" title="f_{SCL}=\frac{f_{clk}}{(2\times CNTR)-26}" /></a>
</p>

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=CNTR=\frac{f_{clk}/f_{SCL}&plus;26}{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CNTR=\frac{f_{clk}/f_{SCL}&plus;26}{2}" title="CNTR=\frac{f_{clk}/f_{SCL}+26}{2}" /></a>
</p>

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=CNTR=\frac{40MHz/100kHz&plus;26}{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CNTR=\frac{40MHz/100kHz&plus;26}{2}" title="CNTR=\frac{40MHz/100kHz+26}{2}" /></a>
</p>

<p align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=CNTR=213" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CNTR=213" title="CNTR=213" /></a>
</p>


> Note: The actual frequency of the I2C clock depends on the rise and fall times of your
circuit. Using the previous equation guarantees that the frequency of the generated
clock signal complies with the I2C specification for standard and fast modes,
regardless of the connected circuit.

### I2C Data Out Registers (I2C.x.DATO)

Register list: I2C.A.DATO, I2C.B.DATO

Data type: U8

This register holds the data that is sent to the slave device during the next send operation.

### I2C Data In Registers (I2C.x.DATI)

Register list: I2C.A.DATI, I2C.B.DATI

Data type: U8

This register holds the data that is received from the slave device during the last receive
operation.

### I2C Status Registers (I2C.x.STAT)

Register list: I2C.A.STAT, I2C.B.STAT

Data type: U8

This register indicates the current status of the I2C subsystem.

| Bit            | 7  | 6  | 5       | 4      | 3       | 2       | 1    | 0    | 
|----------------|----|----|---------|--------|---------|---------|------|------| 
| Name           | -  | -  | BUSBSY  | INUSE  | DATNAK  | ADRNAK  | ERR  | BSY  | 
| Initial Value  | 0  | 0  | 0       | 0      | 0       | 0       | 0    | 0    | 

- Bits [7:6] - Reserved for future use.

- Bit [5] - BUSBSY: I2C bus is busy.

Indicates if the I2C bus is currently busy. The bit is set to 1 when the bus is busy. The
bit is set to 0 when the bus is free.

- Bit [4] - INUSE: I2C subsystem is in use.

Indicates if the I2C subsystem is currently in use. The bit is set to 1 when the
subsystem is in use. The bit is set to 0 when the subsystem is free.

- Bit [3] - DATNAK: Data Not Acknowledge (NAK) received.

Indicates if a NAK is received from the slave after the last data transmission. The bit
is set to 1 when a NAK is received. The bit is set to 0 when a NAK is not received, or
an ACK is received.

- Bit [2] - ADRNAK: Address Not Acknowledge (NAK) received.

Indicates that a NAK is received from the slave after the last address transmission.
The bit is set to 1 when a NAK is received. The bit is set to 0 when a NAK is not
received (an ACK is received).

- Bit [1] - ERR: Error

Indicates that an error occurs during the last transmission. This could be either a
NAK is received on the last data transmission or on the last address transmission. It is
provided for convenience so that both the ADRNAK and DATNAK bits don't have to
be checked every time. When the value = 0 no error occurred during the last
operation, when the value = 1 an error occurred during the last operation. If the value
= 1 the DATNAK and ADRNAK bits must be checked to see the cause of the error.

- Bit [0] - BSY: Busy

Indicates if the I2C subsystem is busy performing an operation. The value is 1 when
the subsystem is busy. The value is 0 when the subsystem is not busy.


<p align="center">
Table 8. I2C busbsy/inuse/bsy combinations  
</p>

| BUSBSY  | INUSE  | BSY  | Interpretation                                                                                                                                           | 
|---------|--------|------|----------------------------------------------------------------------------------------------------------------------------------------------------------| 
| 0       | 0      | 0    | The I2C bus is free and control can be taken by the I2C subsystem.                                                                                       | 
| 1       | 0      | 0    | The I2C bus is busy and in use by some other master connected to the bus. (Not Supported)                                                                | 
| 1       | 1      | 0    | The I2C bus is busy and in use by the I2C subsystem. The subsystem is not busy so the I2C subsystem is either in the TX IDLE, or RX IDLE state.          | 
| 1       | 1      | 1    | The I2C bus is busy, in use by the I2C subsystem, and the subsystem is executing some operation. This could be a START, REPEATED START, TX, RX, or STOP. | 

```
All other combinations have no real-world interpretation and should never occur.
```

### I2C Control Registers (I2C.x.CNTL)

Register list: I2C.A.CNTL, I2C.B.CNTL

Data type: U8

This register controls the next operation to be performed by the I2C subsystem. Some of
the operations supported by the I2C subsystem can be independent of each other. As such
they must be configured to occur before the operation is started. See Table 1 for a list of
valid and invalid values for the CNTL register.

| Bit      | 7  | 6  | 5  | 4  | 3    | 2     | 1      | 0      | 
|----------|----|----|----|----|------|-------|--------|--------| 
| Name     | -  | -  | -  | -  | ACK  | STOP  | START  | TX/RX  | 
| Initial  |    |    |    |    |      |       |        |        | 
| Value    | 0  | 0  | 0  | 0  | 0    | 0     | 0      | 0      | 


- Bits [7:4] - Reserved for future use.

- Bit [3] - ACK: Data Acknowledge Enable

When receiving data from the slave, this bit specifies if an ACK or a NAK must be
generated after the data byte is received. When sending data to the slave device, this
bit is ignored.

> Note: Sending an ACK after the last data byte received (before generating a STOP
condition) violates the I2C standard.

See field decoding in Table 9.

- Bit [2] - STOP: Generate the STOP condition.

Specifies if the I2C subsystem generates a STOP condition after completing the
operation. When the STOP condition is generated, control of the I2C bus is released.

> Note: When receiving data from the slave, the STOP bit and the ACK bit must never
be true at the same time.

See field decoding in Table 9.

- Bit [1] - START: Generate the START condition.

Specifies if the I2C controller generates a START or REPEATED START condition.
A START condition must be generated when the I2C subsystem does not have
control of the bus and wants to get control. A REPEATED START condition must be
generated when the I2C subsystem already has control of the bus and wants to either
change the addressed slave device or change the direction of the transmission to the
same slave device.

>Note: When the START bit is TRUE, the TX/RX bit must also be TRUE.

See field decoding in Table 9.

- Bit [0] - TX/RX: Transmit or receive a data byte.

Specifies if the I2C controller sends a data byte to or receive a data byte from the
slave device. The direction of the transmission (whether it is a send or receive
operation) depends on the value of the R/S bit in the I2C.x.ADDR register. This bit
can be set on its own (when in send mode) or in conjunction with the ACK bit (when
in receive mode) to continually send or receive data from the slave without having to
generate START or STOP conditions.
See field decoding in Table 9.

<p align="center">
Table 9. I2C control registers possible combinations
</p>

| State    | R/S                                       | ACK  | STOP  | START  | TX/RX  | I2C Operation                                                                                                             | 
|----------|-------------------------------------------|------|-------|--------|--------|---------------------------------------------------------------------------------------------------------------------------| 
| IDLE     | 0                                         | X    | 0     | 1      | 1      | Generate START, Send Address, Receive Address ACK, Send Data, Receive Data ACK, and go to TX IDLE state.                  | 
|          | 0                                         | X    | 1     | 1      | 1      | Generate START, Send Address, Receive Address ACK, Send Data, Receive Data ACK, Generate STOP, and return to IDLE state.  | 
|          | 1                                         | 0    | 0     | 1      | 1      | Generate START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, and go to RX IDLE state.                  | 
|          | 1                                         | 0    | 1     | 1      | 1      | Generate START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, and return to IDLE state.                 | 
|          | 1                                         | 1    | 0     | 1      | 1      | Generate START, Send Address, Receive Address ACK, Receive Data, Send Data ACK, and go to RX IDLE state.                  | 
|          | 1                                         | 1    | 1     | 1      | 1      | Illegal. (Master cannot transmit an ACK before generating a STOP.)                                                        | 
|          | All other operations are non-operations.  |    |   |   |   | NOP  |       |        |        |                                                                                                                           | 
| TX IDLE  | X                                         | X    | 0     | 0      | 1      | Send Data (to previously addressed slave),Receive Data ACK, and return to TX IDLE state.                                  | 
|          | X                                         | X    | 1     | 0      | 0      | Generate STOP, and go to IDLE state.                                                                                      | 
|          | X                                         | X    | 1     | 0      | 1      | Send Data, Receive Data ACK, Generate STOP, and go to IDLE state.                                                         | 
|   |0        | X                                         | 0    | 1  | 1  | Generate REPEATED START, Send Address, Receive Address ACK, Send Data, Receive Data ACK, and return to TX IDLE state.  |                                                                                                                                | 
|          | 0                                         | X    | 1  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Send Data, Receive Data ACK, Generate STOP, and go to IDLE state.  | 
|          | 1                                         | 0    | 0  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, and go to RX IDLE state.              | 
|          | 1                                         | 0    | 1  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, Generate STOP, and go to IDLE state.  | 
|          | 1                                         | 1    | 0  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data ACK, and go to RX IDLE state.              | 
|          | 1                                         | 1    | 1  | 1  | 1                                                                                                                      | Illegal. (Master cannot transmit an ACK before generating a STOP.)                                                             | 
|          | All other operations are non-operations.  |    |   |   |   | NOP  |    |    |                                                                                                                        |                                                                                                                                | 
| RX IDLE  | X                                         | 0    | 0  | 0  | 1                                                                                                                      | Receive Data (from previously addressed slave), Send Data NAK, and return to RX IDLE state.                                    | 
|          | X                                         | X    | 1  | 0  | 0                                                                                                                      | Generate STOP, and go to IDLE state.                                                                                           | 
|          | X                                         | 0    | 1  | 0  | 1                                                                                                                      | Receive Data, Send Data NAK, Generate STOP, and return to IDLE state.                                                          | 
|          | X                                         | 1    | 0  | 0  | 1                                                                                                                      | Receive Data, Send Data ACK, and                                                                                               | 
|          |                                           |      |    |    |                                                                                                                        | return to RX IDLE state.                                                                                                       | 
|          | X                                         | 1    | 1  | 0  | 1                                                                                                                      | Illegal. (Master cannot transmit an ACK before generating a STOP.)                                                             | 
|          | 0                                         | X    | 0  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, RX Address ACK, Send Data, RX Data ACK, and go to TX IDLE state.                        | 
|          | 0                                         | X    | 1  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Send Data, Receive Data ACK, Generate STOP, and go to IDLE state.  | 
|          | 1                                         | 0    | 0  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, and return to RX IDLE state.          | 
|          | 1                                         | 0    | 1  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data NAK, Generate STOP, and go to IDLE state.  | 
|          | 1                                         | 1    | 0  | 1  | 1                                                                                                                      | Generate REPEATED START, Send Address, Receive Address ACK, Receive Data, Send Data ACK, and return to RX IDLE state.          | 
|          | 1                                         | 1    | 1  | 1  | 1                                                                                                                      | Illegal. (Master cannot transmit an ACK before generating a STOP.)                                                             | 
|          | All other operations are non-operations.  |    |   |   |   | NOP  |    |    |                                                                                                                        |                                                                                                                                | 


### I2C Execute Registers (I2C.x.GO)

Register list: I2C.A.GO, I2C.B.GO

Data type: Boolean

This register causes the operation specified in the I2C.x.CNTL register to begin. When an operation is written to the CNTL register, it does not start until the GO bit is strobed. The user only has to write a TRUE to this register as the register resets to FALSE after the I2C operation has started. Table 1 shows how to set the CNTL register for the different possible I2C operations.

### I2C Sequence Flowcharts

The following figures show the sequence of events required to use the I2C peripheral.

#### Sending a Single Byte

<p align="center">
    <img src="docs/resources/mdk6.png">
</p>

#### Receiving a Single Byte

<p align="center">
    <img src="docs/resources/mdk7.png">
</p>

#### Sending Multiple Bytes

<p align="center">
    <img src="docs/resources/mdk8.png">
</p>

#### Receiving Multiple Bytes

<p align="center">
    <img src="docs/resources/mdk9.png">
</p>

#### Sending Multiple Bytes then Receiving Multiple Bytes

<p align="center">
    <img src="docs/resources/mdk10.png">
</p>

#### Receiving Multiple Bytes then Sending Multiple Bytes

<p align="center">
    <img src="docs/resources/mdk11.png">
</p>

## UART

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”).

#### UART Enable Register (UART.x.ENA)

Register list: UART.A.ENA, UART.B.ENA

Data type: Boolean 

The UART and console output are multiplexing with the same pin. This register decides whether the UART is enabled for a specific bank.

#### UART Status Register (UART.x.STAT)

Register list: UART.A.STAT, UART.B. STAT 

Data type: Boolean 

This register reads the status of UART whether it is enabled or disabled for a specific bank. 

## IRQ

> Note: When you program in C language, register names must not contain periods, colons, or spaces (like using “DIOA_190DIR” for “DIO.A_19:0.DIR”).

### Timer Interrupt

> Note: Timer Interrupt reserves the IRQ Number 0 while the other interrupts use
values within the range [1 , 8].

#### Timer Read Register (IRQ.TIMER.READ)

Register list: IRQ.TIMER.READ

Data type: U32

This register contains the remaining time before the FPGA timer elapses. The FPGA timer
triggers an interrupt request (IRQ) when IRQ.TIMER.READ counts down to zero. If
IRQ.TIMER.READ is not zero, the FPGA timer counts down to one per microsecond.

#### Timer Write Register (IRQ.TIMER.WRITE)

Register list: IRQ.TIMER.WRITE

Data type: U32

This register attempts to reset the remaining time of the FPGA timer. The value of this
register does not take effect until IRQ.TIMER.SETTIME is strobed.

#### Timer Set Time Register (IRQ.TIMER.SETTIME)

Register list: IRQ.TIMER.SETTIME

Data type: Boolean

This register is the toggle to set the FPGA timer with the value in the IRQ.TIMER.WRITE
register. The default value is FALSE. The write operation starts when you write TRUE to
this register. After one iteration of writing, the register resets to FALSE automatically.

### Analog Input Interrupt

#### Analog IRQ Threshold Register (IRQ.AI_x.THRESHOLD)

Register list: IRQ.AI_A_0.THRESHOLD, IRQ.AI_A_1.THRESHOLD

Data type: FXP

This register sets the value of the analog input threshold. When an analog input signal crosses the threshold, an interrupt is triggered. Each channel has one analog IRQ threshold register.

#### Analog IRQ Hysteresis Register (IRQ.AI_x.HYSTERESIS)

Register list: IRQ.AI_A_0.HYSTERESIS, IRQ.AI_A_1.HYSTERESIS

Data type: FXP

This register sets the value of hysteresis or the window size. Hysteresis adds a window
above or below the analog IRQ threshold to reduce false triggering due to noise. Each
channel has one analog IRQ hysteresis register.

#### Analog IRQ Configuration Register (IRQ.AI_ x.CNFG)

Register list: IRQ.AI_A_3:0.CNFG

Data type: U8

This register contains the interrupt type and enabling configuration of the analog IRQ, as
shown in the following table.

| Bit            | 7  | 6  | 5  | 4  | 3                | 2               | 1                 | 0               | 
|----------------|----|----|----|----|------------------|-----------------|-------------------|-----------------| 
| Name           | -  | -  | -  | -  | IRQ.AI_A_1.Type  | IRQ.AI_A_1.ENA  | IRQ.AI_A_0 .Type  | IRQ.AI_A_0.ENA  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0                | 0               | 0                 | 0               | 

- Bits [7:4] - Reserved for future use.
- Bit [3] - IRQ.AI_A_1. Type.

Specifies the interrupt type of the channel. If the bit is set to 1, the AI1
 channel on bank A checks AI interrupts on a rising edge of the analog input
 signal. If the bit is set to 0, the AI1 channel on bank A checks AI interrupts
 on a falling edge of the analog input signal. 

- Bit [2] - IRQ.AI_A_1. ENA.

Specifies the interrupt type of the channel. If the bit is set to 1, the AI1
 channel on bank A checks AI interrupts on a rising edge of the analog input
 signal. If the bit is set to 0, the AI1 channel on bank A checks AI interrupts
 on a falling edge of the analog input signal. 
 
- Bit [1] - IRQ.AI_A_0. Type.

Specifies the interrupt type of the channel. If the bit is set to 1, the AI0
 channel on bank A checks AI interrupts on a rising edge of the analog input
 signal. If the bit is set to 0, the AI0 channel on bank A checks AI interrupts
 on a falling edge of the analog input signal.

- Bit [0] - IRQ.AI_A_0. ENA

Enables the settings of the analog input interrupt channel. If the bit is set to
 1, the AI0 channel on bank A starts checking AI interrupts based on the
 settings. If the bit is set to 0, the AI0 channel on bank A stops checking AI
 interrupts. The default value of the bit is 0 when the NI ELVIS III device is
 powered on. 

#### Analog IRQ Number Register (IRQ.AI_x.NO)

Register list: IRQ.AI_A_0.NO, IRQ.AI_A_1.NO

Data type: U8

This register specifies the identifier of the interrupt. Each channel has one analog IRQ
number register. The IRQ number ranges from 1 to 8 on FPGA. The number is shared
with analog, digital and button interrupts.

### Digital Input Interrupt

#### Digital Enabling Register (IRQ.DIO_x.ENA)

Register list: IRQ.DIO_A_7:0.ENA

Data type: U8

This register enables the settings of digital input interrupt channels.

| Bit            | 7  | 6  | 5  | 4  | 3                 | 2                | 1                 | 0                | 
|----------------|----|----|----|----|-------------------|------------------|-------------------|------------------| 
| Name           | -  | -  | -  | -  | IRQ.DIO_A _3.ENA  | IRQ.DIO_A_2.ENA  | IRQ.DIO_A _1.ENA  | IRQ.DIO_A_0.ENA  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0                 | 0                | 0                 | 0                | 

- Bits [7:4] - Reserved for future use.
- Bits [3:0] - IRQ.DIO_A_3:0.ENA.

Each bit in Bits [3:0] controls the settings of one channel. For example, in
IRQ.DIO_A_3:0.ENA, bit 0 controls A/DIO0, while bit 3 controls A/DIO3. If the bit is set
to 1, the channel starts checking DI interrupts based on the settings. If the bit is set to 0,
the channel stops checking the interrupt. The default value of the bit is 0 when the NI
ELVIS III device is powered on.

#### Digital Rising Register (IRQ.DIO_x.RISE)

Register list: IRQ.DIO_A_7:0.RISE

Data type: U8

This register enables the digital rising edge interrupt of digital input interrupt channels.

| Bit            | 7  | 6  | 5  | 4  | 3                  | 2                 | 1                  | 0                 | 
|----------------|----|----|----|----|--------------------|-------------------|--------------------|-------------------| 
| Name           | -  | -  | -  | -  | IRQ.DIO_A _3.RISE  | IRQ.DIO_A_2.RISE  | IRQ.DIO_A _1.RISE  | IRQ.DIO_A_0.RISE  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0                  | 0                 | 0                  | 0                 | 

- Bits [7:4] - Reserved for future use.
- Bits [3:0] - IRQ.DIO_A_3:0.RISE.

Each bit in Bits [3:0] controls one channel. For example, in IRQ.DIO_A_3:0.RISE, bit 0
controls A/DIO0, while bit 3 controls A/DIO3. If the bit is set to 1, the channel checks DI
interrupts on a rising edge of the digital input signal. If the bit is set to 0, the channel does
not check the rising edge of the digital input signal.

#### Digital Falling Register (IRQ.DIO_x.FALL)

Register list: IRQ.DIO_A_7:0.FALL

Data type: U8

This register enables the digital falling edge interrupt of digital input interrupt channels.

| Bit            | 7  | 6  | 5  | 4  | 3                  | 2                 | 1                  | 0                 | 
|----------------|----|----|----|----|--------------------|-------------------|--------------------|-------------------| 
| Name           | -  | -  | -  | -  | IRQ.DIO_A _3.FALL  | IRQ.DIO_A_2.FALL  | IRQ.DIO_A _1.FALL  | IRQ.DIO_A_0.FALL  | 
| Initial Value  | 0  | 0  | 0  | 0  | 0                  | 0                 | 0                  | 0                 | 

- Bits [7:4] - Reserved for future use.
- Bits [3:0] - IRQ.DIO_A_3:0.FALL.

Each bit in Bits [3:0] controls one channel. For example, in IRQ.DIO_A_3:0.FALL, bit 0
controls A/DIO0, while bit 3 controls A/DIO3. If the bit is set to 1, the channel checks DI
interrupts on a falling edge of the digital input signal. If the bit is set to 0, the channel does
not check the falling edge of the digital input signal.

#### Digital IRQ Number Register (IRQ.DIO_x.NO)

Register list: IRQ.DIO_A_0.NO, IRQ.DIO_A_1.NO, IRQ.DIO_A_2.NO,
IRQ.DIO_A_3.NO

Data type: U8

This register specifies the identifier of the interrupt. Each channel has one digital IRQ
number register. The IRQ number ranges from 1 to 8 on FPGA. The number is shared
with analog, digital and button interrupts.

#### Digital Count Register (IRQ.DIO_A_0.CNT)

Register list: IRQ.DIO_A_0.CNT, IRQ.DIO_A_1.CNT, IRQ.DIO_A_2.CNT,
IRQ.DIO_A_3.CNT

Data type: U32

This register specifies the number of edges for triggering one interrupt. The interrupt is
triggered every time the edges count reaches the number. Each channel has one digital
count register.

### Button Interrupt

#### Button Enabling Register (IRQ.DI_BTN.ENA)

Register list: IRQ.DI_BTN.ENA

Data type: Boolean

This register enables the settings of the button interrupt channel. If the bit is set to 1, the
channel starts checking interrupts based on the settings. If the bit is set to 0, the channel
stops checking the interrupt. The default value of the bit is 0 when the NI ELVIS III
device is powered on.

#### Button Rising Register (IRQ.DI_BTN.RISE)

Register list: IRQ.DI_BTN.RISE

Data type: Boolean

This register enables the rising edge interrupt of the button channel. If the bit is set to 1,
the channel checks interrupts on a rising edge of the button state. If the bit is set to 0, the
channel does not check the rising edge of the button state.

#### Button Falling Register (IRQ.DI_BTN.FALL)

Register list: IRQ.DI_BTN.FALL

Data type: Boolean

This register enables the falling edge interrupt of the button channel. If the bit is set to 1,
the channel checks interrupts on a falling edge of the button state. If the bit is set to 0, the
channel does not check the falling edge of the button state.

#### Button IRQ Number Register (IRQ.DI_BTN.NO)

Register list: IRQ.DI_BTN.NO

Data type: U8

This register specifies the identifier of the interrupt. The available range of IRQ number is
1~8 on FPGA. The number is shared with analog, digital and button interrupts.

#### Button Count Register (IRQ.DI_BTN.CNT)

Register list: IRQ.DI_BTN.CNT

Data type: U32

This register specifies the number of edges for triggering one interrupt. The interrupt is
triggered every time the edges count reaches the number.

```
Refer to the NI Trademarks and Logo Guidelines at ni.com/trademarks for more information on National
Instruments trademarks. Other product and company names mentioned herein are trademarks or trade names
of their respective companies. For patents covering National Instruments products/technology, refer to
the appropriate location: patents.txt file on your media, or the Help»PatentsNational Instruments Patent
Notice in your software, the at ni.com/patents. You can find information about end-user license
agreements (Refer to the EULAs) and third-party legal notices in the readme file for your NI product.
Export Compliance Information at ni.com/legal/export-compliance for the National Instruments global
trade compliance policy and how to obtain relevant HTS codes, ECCNs, and other import/export data. NI
MAKES NO EXPRESS OR IMPLIED WARRANTIES AS TO THE ACCURACY OF THE INFORMATION CONTAINED HEREIN AND SHALL
NOT BE LIABLE FOR ANY ERRORS. U.S. Government Customers: The data contained in this manual was developed
at private expense and is subject to the applicable limited rights and restricted data rights as set
forth in FAR 52.227-14, DFAR 252.227-7014, and DFAR 252.227-7015. 
 
© 2018 National Instruments. All rights reserved. 2 | ni.com | NI ELVIS III
Shipping Personality 1.0 Reference 
```




