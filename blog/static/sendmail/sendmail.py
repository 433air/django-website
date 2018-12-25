#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

mail_info = {
	"from": "89111876@qq.com",
	"to": "89111876@qq.com",
	"hostname": "smtp.qq.com",
	"username": "89111876",
	"password": "dsxyrfogpijkbiic",
	"mail_subject": "433air的来信",
	#"mail_text": "试试中文乱码",
	"mail_encoding": "utf-8"
}

def sendemail(name, phone, email, message):
	try:
		smtp = SMTP_SSL(mail_info["hostname"])
		smtp.set_debuglevel(1)
		
		mail_text = '''
			来自433air {0} 的留言.
	
			{2}

		---------------------------------------------
			对方邮件:{3}
			对方电话:{1}
		---------------------------------------------	
		'''.format(name, phone, message, email)
		subject = mail_info['mail_subject'] + '_{0}'.format(name)
		smtp.ehlo(mail_info["hostname"])
		smtp.login(mail_info["username"], mail_info["password"])
		msg = MIMEText(mail_text, "plain", mail_info["mail_encoding"])
		msg["Subject"] = Header(subject, mail_info["mail_encoding"])
		msg["from"] = mail_info["from"]
		msg["to"] = mail_info["to"]
		smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
		smtp.quit()
		return True
	except:
		return False

@app.route('/sendemail', methods=['GET', 'POST'])
def send():
	name = request.args.get('name','no name')
	phone = request.args.get('phone','@0000000000000')
	email = request.args.get('email', 'unknow@unknow.com')
	message = request.args.get('message', 'no message')
	if sendemail(name, phone, email, message):
		'1'
	return '1'

if __name__ == "__main__":
	app.run(host = '0.0.0.0')







