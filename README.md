How to use NI ELVIS III with Python
=======  
# Overview
In this document we will walk you through the setup, transfer of files, and the use of a Python example on NI ELVIS III. The NI ELVIS III solution for project-based learning can be programmed with python to help students or educators who are familiar with Python syntax to rapidly acquire measurements using common SSH clients. Attached to this file are a total of 18 examples which illustrate the use of the NI ELVIS III helper library ([academicIO.py](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/source/nielvisiii/academicIO.py)).

# Table of Contents
- [NI ELVIS III Configuration Setup](#ni-elvis-iii-configuration-setup)
  * [Enable the Secure Shell Server](#enable-the-secure-shell-server)
  * [Setup Time Configuration](#setup-time-configuration)
- [Software Setup](#software-setup)
- [File Transfer](#file-transfer)
- [Running the Example](#running-the-example)
- [Function Select Register](#function-select-register)

# NI ELVIS III Configuration Setup

## Enable the Secure Shell Server
1. Open Internet Explorer and visit the NI ELVIS III Configuration website: \<IP Address of NI ELVIS III\>/WIF.html<br />
  :exclamation: IP Address can be found on the Display of the NI ELVIS III. Press BUTTON 0 until IP address appears. Enter IP address from the display.<br />

      ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/IPaddress.jpg)
  
2. Navigate to the ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/system_configuration.png) tab at the left of the page if not already there.
3. Enable **Secure Shell Server (sshd)** checkbox in the **Startup Settings** section.
    ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/sshd.png)
4. Click **Save**.

## Setup Time Configuration
On the NI ELVIS III configuration website:
1. Click on the ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/time_configuration.png) tab at the left of the page .
2. Change the date and time to the current local date and time, and select the right time zone.
3. Click **Save**.

# Software Setup

In this section we will install the software needed to communicate to the NI ELVIS III and install the required packages to use the Python FPGA API.
1. Install the NI Measurement Live Support Files.
2. Connect the NI ELVIS III to the computer via USB, Ethernet or WiFi.
3. Install and open your favorite SSH client. If you do not have one, we recommend [PuTTY](https://the.earth.li/~sgtatham/putty/latest/w32/putty.exe): 
    - Configure PuTTY or another client as follows:
    
        ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/putty.png)
        
        - **Host Name**: \<IP Address of NI ELVIS III\>
        - **Port**: 22
        - **Connection Type**: SSH
    - Click **Open**.
    - Once the connection opens Log In as:
       - **Username**: admin
       - **Password**: (Just press Enter. There is no password by default.)
    - Run the following commands:<br />
       :exclamation: Time configuration must be set before running these commands
        ```
        opkg update
        opkg upgrade
        opkg install python
        opkg install python-pip
        pip install nifpga
        pip install pyvisa
        ```
    - The NI ELVIS III is now setup to run Python applications and communicate to the FPGA using the Python FPGA API.

# File Transfer

In this section we will transfer an FPGA bitfile and the Python examples to the NI ELVIS III. The directions are performed using the free FTP Client FileZilla. You are free to use any application you are comfortable with.
1. Download and install [FileZilla](https://filezilla-project.org/download.php)
2. Log into the NI ELVIS III in FileZilla:
    - **Configuration**:
        
        ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/filezilla.png)
        
        - **Host Name**: sftp://\<IP Address of NI ELVIS III\>
        - **Username**: admin
        - **Password**: (Just press Enter. There is no password by default.)
    - Click **Quickconnect**
3. Navigate to the `/home/admin` directory.
    
    ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/home_directory.png)
    
4. Upload the [ELVIS III v1.1 FPGA.lvbitx](https://github.com/ni-kismet/NI-ELVIS-III-Python/tree/master/bitfile) bitfile, [NI ELVIS III helper library](https://github.com/ni-kismet/NI-ELVIS-III-Python/tree/master/source/nielvisiii), and the [Python examples](https://github.com/ni-kismet/NI-ELVIS-III-Python/tree/master/examples) to the directory `/home/admin` directory in FileZilla.

# Running the Example

In the PuTTY client (or similar clients) used in the earlier **Software Setup** session, enter the following commands:
```
cd /home/admin
python filename.py
```

# Function Select Register

- DIO:      DIO [0:19] on bank A and bank B
- PWM:      DIO [0:19] on bank A and bank B
- Encoder:  DIO [0:1], DIO [2:3], …, DIO [18:19] on bank A and bank B
- SPI:      DIO [5:7] on bank A and bank B
- I2C:      DIO [14:15] on bank A and bank B
- UART:     DIO [16:17]  on bank A and bank B

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
