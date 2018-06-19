How to use the Python FPGA API with the NI ELVIS III
=======
In this document we will walk you through setup, transfer of files, and the use of a Python program. There are a total of 14 Examples included which illustrate the use of the NI ELVIS III Academic IO helper library.

Time Configuration Setup
--------
In this session we will setup the time configuration of the NI ELVIS III.
1. **Open** a browser and visit the NI ELVIS III configuration website: <IP Address of NI ELVIS III>/WIF.html<br />
   :exclamation: IP Address can be found at the top of the NI ELVIS III
2. **Click**   (at the left hand side of the webiste).
3. **Change** the date and time to current time based on your current time zone.
4. **Click** Save.

Software Setup
--------
In this section we will install the software needed to communicate to the NI ELVIS III and install the required packages to use the Python FPGA API.
1. **Install** the NI Measurement Live Support Files.
2. **Connect** the NI ELVIS III using USB or to the internet using the Ethernet Port or the WIFI.
3. **Install** and open your favorite SSH client. If you do not have one, we recommend PuTTY: https://the.earth.li/~sgtatham/putty/latest/w32/putty.exe
    - **Configure** PuTTY or another client as follows:
        - Host Name: _[IP Address of NI ELVIS III]_
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
        * Host Name: sftp://_[IP Address of NI ELVIS III]_
        * Username: admin
        * Password: (Just hit enter, there is no password by default)
    - **Press** “Quickconnect”
3. **Navigate** to the /home/admin directory using: `cd /home/admin`
4. **Download** the “NIELVISIIIPythonExamples.zip”
5. **Extract** the Example files.
6. **Drag** the “ELVIS III v1.1 FPGA.lvbitx” Bitfile into the directory in FileZilla.
7. **Drag** the Python files into the same directory as the Bitfile in FileZilla.

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
with NIELVISIIIAcademicIO.AnalogInput({'bank': bank,
                                       'channel': channel,
                                       'differential': mode}) 
                                                             as AI_single_channel:
```
It is always recommended that you use a Session with a context manager (with). Opening a Session without a context manager could cause you to leak the session if : `Session.close` is not called.
