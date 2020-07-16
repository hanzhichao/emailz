import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import logging
from threading import Thread


class Email(object):
    def __init__(self):
        self.user = os.getenv('SMTP_USER', '')
        self.password = os.getenv('SMTP_PWD', '')
        self.host = os.getenv('SMTP_HOST') or 'smtp.%s' % self.user.split('@')[-1]
        self.port = os.getenv('SMTP_PORT', 25)
        self.ssl = os.getenv('SMTP_SSL', False)

    def config(self, user, password, host=None, port=None, ssl=True):
        self.user = user
        self.password = password
        self.host = host or 'smtp.%s' % self.user.split('@')[-1]
        self.port = port
        self.ssl = ssl

    def test(self):
        server = smtplib.SMTP_SSL(self.host, self.port) if self.ssl else smtplib.SMTP(self.host, self.port)
        server.login(self.user, self.password)
        print('test success')

    def _send_email(self, receivers, msg):
        try:
            server = smtplib.SMTP_SSL(self.host, self.port) if self.ssl else smtplib.SMTP(self.host, self.port)
            server.login(self.user, self.password)
            server.sendmail(self.user, receivers, msg.as_string())
            logging.info("Send email to %s done!" % ','.join(receivers))
        except Exception as ex:
            logging.exception(ex)

    def send(self, subject, receivers, body=None, html=None, template=None, attachments=None, asy=True):
        if not all([self.host, self.user, self.password]):
            raise RuntimeError('Send no email for missing self.host,self.user or self.pwd')

        if isinstance(receivers, str):
            receivers = receivers.split(',')

        if self.port and isinstance(self.port, str):
            try:
                self.port = int(self.port)
            except Exception as ex:
                logging.exception(ex)
                self.port = None

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = ','.join(receivers)

        # handle email body --------------------
        if body:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
        if html:
            msg.attach(MIMEText(html, 'html', 'utf-8'))
        if template:
            if not os.path.isfile(template):
                raise FileNotFoundError('Template file %s not found' % template)
            with open(template, encoding='utf-8') as f:
                msg.attach(MIMEText(f.read().strip(), 'html', 'utf-8'))

        # handle attachments --------------------
        if attachments:
            if isinstance(attachments, str):
                attachments = [attachments]
            for file_path in attachments:
                file_name = os.path.basename(file_path)
                att = MIMEBase('application', 'octet-stream')
                att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
                if os.path.isfile(file_path):
                    try:
                        att.set_payload(open(file_path, 'rb').read())
                        encoders.encode_base64(att)
                    except Exception as ex:
                        logging.exception(ex)
                    else:
                        msg.attach(att)

        # handle receivers --------------------
        if isinstance(receivers, str):
            if ',' in receivers:
                receivers = [receiver.strip() for receiver in receivers.split(',')]
            else:
                receivers = [receivers]

        # send email --------------------
        if asy is True:
            t = Thread(target=self._send_email, args=(receivers, msg))
            t.start()
        else:
            self._send_email(receivers, msg)


email = Email()
