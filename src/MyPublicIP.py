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

if __name__ == '__main__':
    sys.stdout.write("Enter mail service (ex. smtp.aol.com): ")
    server = sys.stdin.readline().rstrip()
    sys.stdout.write("Enter port (ex. 587): ")
    port = sys.stdin.readline().rstrip()
    serverPort = server+":"+port
    sys.stdout.write("Enter account: ")
    username = sys.stdin.readline().rstrip()
    password = getpass.getpass().rstrip()
    sys.stdout.write("Recipient: ")
    recipient = sys.stdin.readline().rstrip()
    nat_type, external_ip, external_port = stun.get_ip_info()
    msg = MIMEText(external_ip)
    msg['Subject'] = "[PublicIP] My Public IP Address"
    msg['From'] = username
    msg['To'] = recipient
    
    try:
        mailServer = smtplib.SMTP(serverPort)
        try:
            mailServer.login(username,password)
            try:
                mailServer.sendmail(username,recipient,msg.as_string())
                print "Mail sent. Public IP is %s" % external_ip
            except (smtplib.SMTPRecipientsRefused,smtplib.SMTPHeloError,smtplib.SMTPSenderRefused,smtplib.SMTPDataError) as e:
                print "Could not send message to %s" % recipient
        except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPException) as e:
            print "Could not log in to: %s" % serverPort
        mailServer.quit()
    except (smtplib.SMTPConnectError,socket.error) as e:
        print "Could not connect to server: %s" % serverPort
    
    