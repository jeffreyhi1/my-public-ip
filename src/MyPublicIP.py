'''
Created on Feb 28, 2014

@author: Daniel Rosen
'''

import smtplib
import sys
import getpass
from socket import error as sockerror
from email.mime.text import MIMEText
import argparse
import time
import datetime
import logging
import signal

try:
    import stun
except (ImportError):
    sys.stderr.write("Error: you must install pystun: https://pypi.python.org/pypi/pystun")
    sys.exit()
    
version = "1.0"

def mailIP(external_ip,timestamp):
    body = "IP: "+external_ip+"\nTime: "+datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    msg = MIMEText(body)
    msg['Subject'] = "[PublicIP] My Public IP Address"
    msg['From'] = username
    msg['To'] = recipient
    
    try:
        mailServer = smtplib.SMTP_SSL(serverPort)
        try:
            mailServer.login(username,password)
            try:
                mailServer.sendmail(username,recipient,msg.as_string())
                logger.info("Mail sent to %s" % recipient)
            except (smtplib.SMTPRecipientsRefused,smtplib.SMTPHeloError,smtplib.SMTPSenderRefused,smtplib.SMTPDataError):
                logger.error("Could not send message to %s" % recipient)
        except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPException):
            logger.error("Could not log in to: %s" % serverPort)
        try:
            mailServer.quit()
        except (smtplib.SMTPServerDisconnected):
            logger.error("Server disconnect early.")
    except (smtplib.SMTPConnectError,sockerror):
        logger.error("Could not connect to server: %s" % serverPort)


def exit_handler(signal,frame):
    logger.info("Server Stopped")
    sys.exit()

def getAccount():
    sys.stdout.write("Enter account: ")
    username = sys.stdin.readline().rstrip()
    password = getpass.getpass().rstrip()
    sys.stdout.write("Recipient: ")
    recipient = sys.stdin.readline().rstrip()
    return username,password,recipient

def saveAccount(filename,username,password,recipient):
    print "Saving account to file not yet implemented"
    
def loadAccount(filename):
    print "Loading account from file not yet implemented"
    return "test","test","test"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Public IP Address via Email',epilog='Author: Dan Rosen')
    parser.add_argument('-m','--minutes',type=int,default=60)
    parser.add_argument('-s','--server',default="smtp.aol.com")
    parser.add_argument('-p','--port')
    parser.add_argument('-l','--log',default="my_public_ip.log")
    parser.add_argument('-f','--file',default=None)
    parser.add_argument('-v','--save',action="store_true", help="requires filename")
    parser.add_argument('--version',action='version',version='Version: %s' % version)
    args = parser.parse_args()
    
    logger = logging.getLogger('my_public_ip')
    logger.setLevel(logging.INFO)
    logfh = logging.FileHandler(args.log)
    logfh.setLevel(logging.INFO)
    logch = logging.StreamHandler()
    logch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logfh.setFormatter(formatter)
    logch.setFormatter(formatter)
    logger.addHandler(logfh)
    logger.addHandler(logch)
    
    if(args.save is True):
        if(args.file is None):
            sys.exit("Saving file requires a filename.")
        else:
            username,password,recipient = getAccount()
            saveAccount(args.file,username,password,recipient)
    else:
        if(args.file is None):
            username,password,recipient = getAccount()
        else:
            username,password,recipient = loadAccount(args.file)
    
    sleeptime = args.minutes*60
    if(args.port is None):
        serverPort = args.server
    else:
        serverPort = args.server+":"+str(args.port)
    external_ip = ""
    logger.info("Server Started")
    signal.signal(signal.SIGINT, exit_handler)
    print 'Press Ctrl+C to exit'
    while True:
        timestamp = time.time()
        logger.info('STUN request at %s' % datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        nat_type, new_external_ip, external_port = stun.get_ip_info()
        if(new_external_ip is None):
            logger.error('STUN request failed')
        elif(new_external_ip != external_ip):
            logger.info('New IP address %s' % new_external_ip)
            mailIP(new_external_ip,timestamp)
        external_ip = new_external_ip
        time.sleep(sleeptime)
    