'''
Created on Feb 28, 2014

@author: Daniel Rosen
'''
import stun
import smtplib
import sys
import getpass

if __name__ == '__main__':
    sys.stdout.write("Enter account: ")
    username = sys.stdin.readline().rstrip()
    password = getpass.getpass().rstrip()
    nat_type, external_ip, external_port = stun.get_ip_info()
    print external_ip
    mailServer = smtplib.SMTP('smtp.aol.com:587')
    mailServer.login(username,password)
    mailServer.sendmail(username,username,external_ip)
    mailServer.quit()
    print "Mail Sent."