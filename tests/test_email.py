import os
from emailz import email

SMTP_PWD = os.getenv('SMTP_PWD') or 'hanzhichao123'  # todo 隐藏


def test_email_send():
    email.config(user='ivan-me@163.com', password=SMTP_PWD)
    email.send(subject='Subject', body='Hello,Emailz', receivers=['hanzhichao@secoo.com'])


def test_email_test():
    email.config(user='ivan-me@163.com', password=SMTP_PWD)
    email.test()


def test_email_send_html():
    email.config(user='ivan-me@163.com', password=SMTP_PWD)
    email.send(subject='Subject', html='<h1>Hello,Emailz</h1>', receivers=['hanzhichao@secoo.com'])


def test_email_send_template():
    email.config(user='ivan-me@163.com', password=SMTP_PWD)
    email.send(subject='Subject', template='tests/template.html', receivers=['hanzhichao@secoo.com'])


def test_email_send_attachments():
    email.config(user='ivan-me@163.com', password=SMTP_PWD)
    email.send(subject='Subject', attachments='tests/template.html', receivers=['hanzhichao@secoo.com'])


def test_email_send_attachments_with_zh_CN():
    email.config(host='smtp.exmail.qq.com', port=465, user='rpa@secoo.com', password='Youxiang_00137')
    email.send(subject='Subject', attachments=['tests/模板.html','tests/template.html'], receivers=['hanzhichao@secoo.com'])