"""
November 2 2020
Qiming Huang

It's a repace for the ddns by automatically check id the current 
ip address is changed. If changed, send the new ip address to email
"""

from requests_html import HTMLSession
import smtplib
from email.mime.text import MIMEText
import time

# current_ip = '49.72.58.66'
mail_host = 'xxx'                       # mail server address for example, smtp.163.com
mail_user = '13324811901'
mail_pass = 'xxx'                       # password provided by mail server (not account password)

sender = '13324811901@163.com'
receivers = ['727534525@qq.com']
url = 'http://cip.cc'                   # website to get the ip address 
cot = 0

from requests.exceptions import ConnectionError

def sleep_time(hour, min, sec):
    return hour*3600 + min*60 + sec

wait_time = sleep_time(0,2,0) # define the sleeping time

while True: # get the ip address
    session = HTMLSession()
    try:
        r = session.get(url)
        about = r.html.find('pre', first=True)
    except ConnectionError:
        print('No Network!!')
        time.sleep(wait_time)
        continue
    try:
        with open('ip_address.txt') as fr:
            current_ip = fr.readline()
            ip_address = about.text.split(' ')[2]
    except AttributeError:
        continue
    if ip_address == current_ip:
        print('ip address did not change! times:' + str(cot))
    else: # if ip address changed, send email
        message = MIMEText(ip_address, 'plain', 'utf-8')
        message['Subject'] = 'ip address'
        message['From'] = sender
        message['To'] = receivers[0]
        with open('ip_address.txt', 'w') as fr:
            fr.write(ip_address)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            print('successfully send new ip_address, it was:' + ip_address)
        except smtplib.SMTPException as e:
            print('Error')

    cot += 1
    time.sleep(wait_time)
