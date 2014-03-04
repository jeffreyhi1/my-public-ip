'''
Created on Feb 28, 2014

@author: Daniel Rosen
'''
import stun
import smtplib
import sys
import getpass
import socket
from email.mime.text import MIMEText
import argparse
import time
import datetime
import logging

def mailIP(external_ip,timestamp):
    body = "IP: "+external_ip+"\nTime: "+datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    msg = MIMEText(body)
    msg['Subject'] = "[PublicIP] My Public IP Address"
    msg['From'] = username
    msg['To'] = recipient
    
    try:
        mailServer = smtplib.SMTP(serverPort)
        try:
            mailServer.login(username,password)
            try:
                mailServer.sendmail(username,recipient,msg.as_string())
                logger.info("Mail sent to %s" % recipient)
            except (smtplib.SMTPRecipientsRefused,smtplib.SMTPHeloError,smtplib.SMTPSenderRefused,smtplib.SMTPDataError):
                logger.error("Could not send message to %s" % recipient)
        except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPException):
            logger.error("Could not log in to: %s" % serverPort)
        mailServer.quit()
    except (smtplib.SMTPConnectError,socket.error):
        logger.error("Could not connect to server: %s" % serverPort)
    
if __name__ == '__main__':
    logger = logging.getLogger('my_public_ip')
    logger.setLevel(logging.INFO)
    logfh = logging.FileHandler('my_public_ip.log')
    logfh.setLevel(logging.INFO)
    logch = logging.StreamHandler()
    logch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logfh.setFormatter(formatter)
    logch.setFormatter(formatter)
    logger.addHandler(logfh)
    logger.addHandler(logch)
    
    parser = argparse.ArgumentParser(description='Timing')
    parser.add_argument('-m','--minutes',type=int,default=60)
    parser.add_argument('-s','--server',default="smtp.aol.com")
    parser.add_argument('-p','--port',type=int,default=587)
    args = parser.parse_args()
    sleep = args.minutes*60
    serverPort = args.server+":"+str(args.port)
    sys.stdout.write("Enter account: ")
    username = sys.stdin.readline().rstrip()
    password = getpass.getpass().rstrip()
    sys.stdout.write("Recipient: ")
    recipient = sys.stdin.readline().rstrip()
    external_ip = ""
    while True:
        timestamp = time.time()
        logger.info('STUN request at %s' % datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        nat_type, new_external_ip, external_port = stun.get_ip_info()
        if(new_external_ip is None):
            logger.error('STUN Failed')
        elif(new_external_ip != external_ip):
            logger.info('New IP Address %s' % new_external_ip)
            mailIP(new_external_ip,timestamp)
        external_ip = new_external_ip
        time.sleep(sleep)
    