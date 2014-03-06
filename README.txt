usage: python MyPublicIP.py -m MINUTES -s SMTP_SERVER -p SMTP_PORT -l LOG
defaults: 60 minutes, smtp.aol.com, 465, my-public-ip.log

Project repository
git clone https://danrosen25@code.google.com/p/my-public-ip/ 

Prerequisites
1. Install Python: http://www.python.org/download/
2. Install setuptools module: https://pypi.python.org/pypi/setuptools (if needed)
3. Install pystun module: https://pypi.python.org/pypi/pystun

Instructions
1. execute the script: python MyPublicIP.py
2. enter smtp account (example: dan15lw@aol.com)
3. enter account password
4. enter destination email address (example: dan15lw@aol.com)
5. move process to background
     a. Ctrl-Z (suspend)
     b. bg PROCESS
6. let run indefinitely
7. To terminate
     option a. kill -9 PROCESS
     option b. fg PROCESS (move to foreground) then Ctrl-X

Notes:
- you can check the log file my-public-ip.log to track what's going on
- it takes about 1.7% of the raspberry pi's memory (8.7 MB) and spends the majority of its life sleeping.  I'll reduce the memory usage later.
- I've only tested this on unix machines but the script probably works in Windows
- I may in the future make it possible to stick the smtp account,password and destination email in an encrypted file so that you do not have to start the process in foreground