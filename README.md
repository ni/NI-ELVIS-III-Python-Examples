How to use the Python FPGA API with the NI ELVIS III
=======
In this document we will walk you through setup, transfer of files, and the use of a Python program. There are a total of 14 Examples included which illustrate the use of the NI ELVIS III Academic IO helper library.

Time Configuration Setup
--------
In this session we will setup the time configuration of the NI ELVIS III.
1. **Open** a browser and visit the NI ELVIS III configuration website: \<IP Address of NI ELVIS III\>/WIF.html<br />
   :exclamation: IP Address can be found at the top of the NI ELVIS III
2. **Click**  ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/time_configuration.png) (at the left hand side of the webiste).
3. **Change** the date and time to current time based on your current time zone.
4. **Click** Save.

Software Setup
--------
In this section we will install the software needed to communicate to the NI ELVIS III and install the required packages to use the Python FPGA API.
1. **Install** the NI Measurement Live Support Files.
2. **Connect** the NI ELVIS III using USB or to the internet using the Ethernet Port or the WIFI.
3. **Install** and open your favorite SSH client. If you do not have one, we recommend PuTTY: https://the.earth.li/~sgtatham/putty/latest/w32/putty.exe
    - **Configure** PuTTY or another client as follows:
    
        ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/putty.png)
        
        - Host Name: \<IP Address of NI ELVIS III\>
        - Port: 22
        - Connection Type: SSH
    - **Press** “Open”
    - Once the connection opens **Log In** as:
       - Username: admin
       - Password: (Just hit enter, there is no password by default)
    - **Run** the following Commands:<br />
       :exclamation: time configuration must be set before running these commands
        ```
        opkg update
        opkg upgrade
        opkg install python
        opkg install python-pip
        pip install nifpga
        pip install pyvisa
        ```
    - The NI ELVIS III is now setup to run Python applications and communicate to the FPGA using the NI FPGA API.

File Transfer
--------
In this section we will transfer an FPGA Bitfile and the Python Example program to the NI ELVIS III. The directions are performed using the free FTP Client FileZilla. You are free to use any application you are comfortable with.
1. **Download** and **Install** FileZilla: https://filezilla-project.org/download.php 
2. **Log Into** the NI ELVIS III in FileZilla:
    - **Configuration**:
        
        ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/filezilla.png)
        
        * Host Name: sftp://\<IP Address of NI ELVIS III\>
        * Username: admin
        * Password: (Just hit enter, there is no password by default)
    - **Press** “Quickconnect”
3. **Navigate** to the /home/admin directory
    
    ![](https://github.com/ni-kismet/NI-ELVIS-III-Python/blob/master/docs/resource/home_directory.png)
    
4. **Upload** the [ELVIS III v1.1 FPGA.lvbitx](https://github.com/ni-kismet/NI-ELVIS-III-Python/tree/master/bitfile) Bitfile and [Python examples](https://github.com/ni-kismet/NI-ELVIS-III-Python/tree/master/source) into the directory `/home/admin` in FileZilla.

Running the Example
--------
In the PuTTY Client or similar opened in Software Setup Enter the following commands:
```
cd /home/admin
python filename.py
```

Open a Session 
--------
Session, a convenient wrapper around the NI ELVIS III controlling APIs.
Example session usage:
```
with academicIO.AnalogInput({'bank': bank,
                             'channel': channel,
                             'mode': mode}) as AI_single_channel:
```
It is always recommended that you use a Session with a context manager (with). Opening a Session without a context manager could cause you to leak the session if : `Session.close` is not called.

Function Select Register 
--------
| NI ELVIS III | DIO | PWM | Encoder | SPI | I2C | UART | 
|:------------:|:-----------:|:-----------:|:---------------:|:-----------:|:------------------------:|:----------:| 
| DIO 0        | DIO 0       | PWM 0       | ENC.A 0         |             |                          |            | 
| DIO 1        | DIO 1       | PWM 1       | ENC.B 0         |             |                          |            | 
| DIO 2        | DIO 2       | PWM 2       | ENC.A 1         |             |                          |            | 
| DIO 3        | DIO 3       | PWM 3       | ENC.B 1         |             |                          |            | 
| DIO 4        | DIO 4       | PWM 4       | ENC.A 2         |             |                          |            | 
| DIO 5        | DIO 5       | PWM 5       | ENC.B 2         | SPI.CLK     |                          |            | 
| DIO 6        | DIO 6       | PWM 6       | ENC.A 3         | SPI.MISO    |                          |            | 
| DIO 7        | DIO 7       | PWM 7       | ENC.B 3         | SPI.MOSI    |                          |            | 
| DIO 8        | DIO 8       | PWM 8       | ENC.A 4         |             |                          |            | 
| DIO 9        | DIO 9       | PWM 9       | ENC.B 4         |             |                          |            | 
| DIO 10       | DIO 10      | PWM 10      | ENC.A 5         |             |                          |            | 
| DIO 11       | DIO 11      | PWM 11      | ENC.B 5         |             |                          |            | 
| DIO 12       | DIO 12      | PWM 12      | ENC.A 6         |             |                          |            | 
| DIO 13       | DIO 13      | PWM 13      | ENC.B 6         |             |                          |            | 
| DIO 14       | DIO 14      | PWM 14      | ENC.A 7         |             | I2C.SCL                  |            | 
| DIO 15       | DIO 15      | PWM 15      | ENC.B 7         |             | I2C.SDA                  |            | 
| DIO 16       | DIO 16      | PWM 16      | ENC.A 8         |             |                          | UART.RX    | 
| DIO 17       | DIO 17      | PWM 17      | ENC.B 8         |             |                          | UART.TX    | 
| DIO 18       | DIO 18      | PWM 18      | ENC.A 9         |             |                          |            | 
| DIO 19       | DIO 19      | PWM 19      | ENC.B 9         |             |                          |            |
