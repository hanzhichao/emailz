import os
from emailz import email


SMTP_USER, SMTP_PWD = os.getenv('SMTP_USER'), os.getenv('SMTP_PWD')
print(SMTP_USER, SMTP_PWD)

def test_email_send():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.send(subject='Subject', body='Hello,Emailz', receivers=['hanzhichao@secoo.com'], asy=False)
    print('........')


def test_email_test():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.test()


def test_email_send_html():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.send(subject='Subject', html='<h1>Hello,Emailz</h1>', receivers=['hanzhichao@secoo.com'])


def test_email_send_template():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.send(subject='Subject', template='tests/template.html', receivers=['hanzhichao@secoo.com'])


def test_email_send_attachments():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.send(subject='Subject', attachments='tests/template.html', receivers=['hanzhichao@secoo.com'])


def test_email_send_attachments_with_zh_CN():
    email.config(host='smtp.exmail.qq.com', port=465, user=SMTP_USER, password=SMTP_PWD)
    email.send(subject='Subject', attachments=['tests/模板.html','tests/template.html'], receivers=['hanzhichao@secoo.com'], asy=False)


if __name__ == '__main__':
    test_email_send()