#!/usr/bin/env python
#coding: utf-8

import smtplib
import email
import mimetypes
import json
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

with open("./conf/config.json", "r") as f:
    config = json.loads(f.read())

mail_host = config["mail_config"]["host"]
mail_user = config["mail_config"]["user"]
mail_pwd = config["mail_config"]["pwd"]
mail_postfix =  config["mail_config"]["postfix"]

def sendmail(to_list,subject,content):
  # translation
	me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEMultipart('related')
	msg['Subject'] = email.Header.Header(subject,'utf-8')
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	msg.preamble = 'This is a multi-part message in MIME format.'
	msgAlternative = MIMEMultipart('alternative')
	msgText = MIMEText(content, 'plain', 'utf-8')
	msgAlternative.attach(msgText)
	msg.attach(msgAlternative)
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user,mail_pwd)
		s.sendmail(me, to_list, msg.as_string())
		s.quit() 
	except Exception,e:
		print e
		return False
	return True
	
def sendhtmlmail(to_list,subject,content):
  # translation
	me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEMultipart('related')
	msg['Subject'] = email.Header.Header(subject,'utf-8')
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	msg.preamble = 'This is a multi-part message in MIME format.'
	msgAlternative = MIMEMultipart('alternative')
	msgText = MIMEText(content, 'html', 'utf-8')
	msgAlternative.attach(msgText)
	msg.attach(msgAlternative)
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.login(mail_user,mail_pwd)
		s.sendmail(me, to_list, msg.as_string())
		s.quit() 
	except Exception,e:
		print e
		return False
	return True

if __name__ == '__main__':
	if sendmail(['546674175@qq.com'],"测试邮件","测试python发送网易邮件"):
		print "Success!"
	else:
		print "Fail!"
