How to Program [NI ELVIS III](http://www.ni.com/en-us/shop/select/ni-elvis) with Python
=======

<p align="center"><img width="700px" src="https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/ni_elvis_iii.png"/></p>

# Overview
In this document we will walk you through the setup, transfer of files, and the use of a Python example on the NI ELVIS III. The NI ELVIS III solution for project-based learning can be programmed with python to help students or educators who are familiar with Python syntax to rapidly acquire measurements by using common SSH clients. Attached to this file are a total of 18 examples which illustrate the use of the NI ELVIS III helper library ([academicIO.py](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/nielvis/academicIO.py)).

NI-ELVIS-III-Python-Examples supports Python 3.4+.

# Table of Contents
- [Software Setup](#software-setup)
  * [Configuring the NI ELVIS III Device](#configuring-the-ni-elvis-iii-device)
  * [Installing Prerequisite Software for NI ELVIS III Python](#installing-prerequisite-software-for-ni-elvis-iii-python)
  * [Installing NI ELVIS III Python Examples](#installing-ni-elvis-iii-python-examples)
    + [Download ZIP File and Upload to the Device via SFTP](#download-zip-file-and-upload-to-the-device-via-sftp)
- [Running the Example](#running-the-example)
- [Examples Overview](#examples-overview)
  * [Analog](#analog)
  * [Bus](#bus)
  * [Digital](#digital)
  * [Interrupt](#interrupt)
- [Opening a Session](#opening-a-session)
- [Function Select Register](#function-select-register)
- [NI ELVIS III Shipping Personality Reference](#ni-elvis-iii-shipping-personality-reference)

<p align="right"><a href="#top">↥ back to top</a>

# Software Setup

## Configuring the NI ELVIS III Device
In this section we will install the NI Measurement Live Support Files and set up the software environment for the NI ELVIS III.

1. Install the [NI Measurement Live Support Files](https://www.ni.com/en-us/support/downloads/software-products/download.measurements-live.html).
2. Connect the NI ELVIS III to the Internet by using the [Ethernet](http://www.ni.com/documentation/en/ni-elvis-iii/latest/getting-started/connecting-device-via-ethernet/#GUID-816EF92E-4CB5-47AA-BDE3-7CF57758FB0E) or [Wireless Network](http://www.ni.com/documentation/en/ni-elvis-iii/latest/getting-started/connnecting-device-via-wireless-network/#GUID-14BF448A-CC19-4DF5-915E-6ED43E5B63E9) so that the Python libraries can be installed from the Internet. We recommend that you use Ethernet Port.
3. Open **Internet Explorer** and visit the NI ELVIS III Configuration website: \<IP Address of the NI ELVIS III\>/WIF.html<br/>
   ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/open_setup_page.gif)
   *Note:* The IP Address can be found on the OLED display of the NI ELVIS III. Press [BUTTON 0](https://www.ni.com/documentation/en/ni-elvis-iii/latest/getting-started/user-programmable-button/) until the IP address appears. Enter the IP address from the display.<br />
4. Enable the **Secure Shell Server** and click **Restart** to restart the device.
   ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/open_ssh.gif)
5. Set up **Time Configuration**. Configure the **Date**, **Current time**, and **Time Zone** to your current local time.
   ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/set_time_zone.gif)
   
   *Note:*
      - Make sure there is a blue mark at the date you selected.
      - You have to set the **Time Configuration** again after you restart the device.
6. Install NI-VISA through **NI MAX** custom software installation if you want to run the UART example.

## Installing Prerequisite Software for NI ELVIS III Python
In this section we will install the software needed to execute the NI ELVIS III Python examples and the required packages to use the Python FPGA API.

1. Install and open your favorite SSH client. If you do not have one, we recommend that you use [PuTTY](https://the.earth.li/~sgtatham/putty/latest/w32/putty.exe):
   ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/putty_connect_to_device.gif)
   - Configure PuTTY or another client as follows:
      - **Host Name**: \<IP Address of the NI ELVIS III\>
      - **Port**: 22
      - **Connection Type**: SSH
   - Once the connection opens, log in as:
       - **login as**: admin
       - **Password**: (Just press **Enter**. There is no password by default.)
2. Install prerequisite software by running the following commands:<br />
   
   *Note:* **Time configuration** must be set before running these commands. If you got any error when downloading **nifpga**, make sure your **Time configuration** of the NI ELVIS III is set correctly.

     ```
     opkg update
     opkg install python3
     opkg install python3 python3-misc
     curl https://bootstrap.pypa.io/get-pip.py | python3
     pip install nielvis
     ```

## Installing NI ELVIS III Python Examples 

In this section we will download the NI ELVIS III Python Examples. 

### Download ZIP File and Upload to the Device via SFTP

1. Open the [NI ELVIS III Python Examples](https://github.com/ni/NI-ELVIS-III-Python-Examples) on GitHub.
2. Download the NI ELVIS III Python helper library and Python Examples from GitHub and unzip it.
   1. Download the Example.
   ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/download_from_github.gif)
   
   3. Unzip the file you just downloaded.
   
      ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/unzip_folder.gif)
      
3. Transfer the NI ELVIS III Python Examples to your NI ELVIS III device.

    - Option 1: Transfer files through scp.

      ```
      scp -r <folder_name> admin@<id_address>:/home/admin/
      ```

      For example: `scp -r NI-ELVIS-III-Python-Examples/ admin@172.22.11.2:/home/admin/`

      *Note:* **Password**: (Blank. There is no password by default.)

   - Option 2: Transfer files through FileZilla.

      1. Download and install [FileZilla](https://filezilla-project.org/download.php). You are free to use any other application you are comfortable with to transfer files.
      2. Configure FileZilla as the following:
   
         ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/filezilla_connect_to_device.gif)
      
         - **Host**: \<IP Address of the NI ELVIS III\>
         - **Username**: admin
         - **Password**: (Blank. There is no password by default.)
         - **Port**: 22

      3. Upload **NI-ELVIS-III-Python-Examples-master/** into the directory `/home/admin`.
      
         ![](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/docs/resource/filezilla_transfer_folder.gif)

<p align="right"><a href="#top">↥ back to top</a>

# Running the Example

1. In the same directory where you upload your example folder to, enter the following command to go to the NI-ELVIS-III-Python example directory.
   ```
   cd NI-ELVIS-III-Python-Examples-master/
   ```
2. Run the example:

   ```
   python examples/<example_category>/<example_filename>.py
   ```
   For example: `python examples/analog/AI_singleChannel.py`.      
   
   *Note:* Make sure your application broad is powered on before running any example.

<p align="right"><a href="#top">↥ back to top</a>

# Examples Overview
  Go to the comments area at the top of each example to see more details. Click the following links to jump into the example page.

 ### [Analog](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/)
   - [AI_configurationOptions](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/AI_configurationOptions.py)
   - [AI_multipleChannels](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/AI_multipleChannels.py)
   - [AI_singleChannel](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/AI_singleChannel.py)
   - [AO_multipleChannels](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/AO_multipleChannels.py)
   - [AO_singleChannel](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/analog/AO_singleChannel.py)
     #### Related Information
       [1 Sample, N Samples, and Continuous Modes](docs/1_Sample_N_Samples_and_Continuous_Modes.md)
 ### [Bus](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/bus)
   - [Encoder](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/bus/Encoder.py)
   - [I2C](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/bus/I2C.py)
   - [SPI](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/bus/SPI.py)
   - [UART](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/bus/UART.py)
 ### [Digital](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital)
   - [Button](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital/Button.py)
   - [DIO_multipleChannels](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital/DIO_multipleChannels.py)
   - [DIO_singleChannel](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital/DIO_singleChannel.py)
   - [LED](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital/LED.py)
   - [PWM](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/digital/PWM.py)
 ### [Interrupt](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/interrupt)
   - [AIIRQ (Analog Interrupt)](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/interrupt/AIIRQ.py)
   - [ButtonIRQ (Button Interrupt)](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/interrupt/ButtonIRQ.py)
   - [DIIRQ (Digital Interrupt)](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/interrupt/DIIRQ.py)
   - [TimerIRQ (Timer Interrupt)](https://github.com/ni/NI-ELVIS-III-Python-Examples/blob/master/examples/interrupt/TimerIRQ.py)

<p align="right"><a href="#top">↥ back to top</a>

# Opening a Session

A context manager ('with' statement) is a convenient way to open/close an NI ELVIS III FPGA session. 
```python
with academicIO.AnalogInput({'bank': ai_bank,
                             'channel': ai_channel,
                             'range': ai_range,
                             'mode': ai_mode}) as AI_single_channel:
```
It is always recommended that you use a context manager to open/close an NI ELVIS III FPGA session. The program will automatically initialize the environment of NI ELVIS III FPGA at the beginning and will automatically free its resources after the 'with' statement ends. Opening a session without a context manager could increase the risk of leaking the session.

See [compound statements](https://docs.python.org/2.7/reference/compound_stmts.html#the-with-statement) for more details about the context manager.

You can also manually open/close an NI ELVIS III FPGA session by using the following commands:
```python
# open a session
AI_single_channel = academicIO.AnalogInput()

# close a session
AI_single_channel.close()
```
If you don’t call the `close()` function after the Python program closes, you may leak the session and cause errors when you run the program again. If you want the FPGA to keep executing the code after the Python program ends, do not call the `close()` function in the Python program.

<p align="right"><a href="#top">↥ back to top</a>

# Function Select Register

- DIO:      DIO [0:19] on bank A and bank B
- PWM:      DIO [0:19] on bank A and bank B
- Encoder:  DIO [0:1], DIO [2:3], …, DIO [18:19] on bank A and bank B
- SPI:      DIO [5:7] on bank A and bank B
- I2C:      DIO [14:15] on bank A and bank B
- UART:     DIO [16:17] on bank A and bank B

|**NI ELVIS III**| DIO | PWM | Encoder | SPI | I2C | UART | 
|:--------------:|:-----------:|:-----------:|:---------------:|:-----------:|:------------------------:|:----------:| 
| **DIO 0**      | DIO 0       | PWM 0       | ENC.A 0         |             |                          |            | 
| **DIO 1**      | DIO 1       | PWM 1       | ENC.B 0         |             |                          |            | 
| **DIO 2**      | DIO 2       | PWM 2       | ENC.A 1         |             |                          |            | 
| **DIO 3**      | DIO 3       | PWM 3       | ENC.B 1         |             |                          |            | 
| **DIO 4**      | DIO 4       | PWM 4       | ENC.A 2         |             |                          |            | 
| **DIO 5**      | DIO 5       | PWM 5       | ENC.B 2         | SPI.CLK     |                          |            | 
| **DIO 6**      | DIO 6       | PWM 6       | ENC.A 3         | SPI.MISO    |                          |            | 
| **DIO 7**      | DIO 7       | PWM 7       | ENC.B 3         | SPI.MOSI    |                          |            | 
| **DIO 8**      | DIO 8       | PWM 8       | ENC.A 4         |             |                          |            | 
| **DIO 9**      | DIO 9       | PWM 9       | ENC.B 4         |             |                          |            | 
| **DIO 10**     | DIO 10      | PWM 10      | ENC.A 5         |             |                          |            | 
| **DIO 11**     | DIO 11      | PWM 11      | ENC.B 5         |             |                          |            | 
| **DIO 12**     | DIO 12      | PWM 12      | ENC.A 6         |             |                          |            | 
| **DIO 13**     | DIO 13      | PWM 13      | ENC.B 6         |             |                          |            | 
| **DIO 14**     | DIO 14      | PWM 14      | ENC.A 7         |             | I2C.SCL                  |            | 
| **DIO 15**     | DIO 15      | PWM 15      | ENC.B 7         |             | I2C.SDA                  |            | 
| **DIO 16**     | DIO 16      | PWM 16      | ENC.A 8         |             |                          | UART.RX    | 
| **DIO 17**     | DIO 17      | PWM 17      | ENC.B 8         |             |                          | UART.TX    | 
| **DIO 18**     | DIO 18      | PWM 18      | ENC.A 9         |             |                          |            | 
| **DIO 19**     | DIO 19      | PWM 19      | ENC.B 9         |             |                          |            |

<p align="right"><a href="#top">↥ back to top</a>

# NI ELVIS III Shipping Personality Reference 

This document contains reference information about the NI ELVIS III shipping personality. The reference includes information about the registers used to control the peripherals of NI ELVIS III.

You can find NI ELVIS III Shipping Personality Reference [here](docs/NI_ELVIS_III_Shipping_Personality_Reference.md).

<p align="right"><a href="#top">↥ back to top</a>
