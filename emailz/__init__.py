import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


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

    def send(self, subject, receivers, body=None, html=None, template=None, attachments=None):
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
                if os.path.isfile(file_path):
                    try:
                        att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
                    except Exception as ex:
                        logging.exception(ex)
                    else:
                        att['Content-Type'] = 'application/octet-stream'
                        att["Content-Disposition"] = f'attachment; filename={os.path.basename(file_path)}'
                        msg.attach(att)

        # handle receivers --------------------
        if isinstance(receivers, str):
            if ',' in receivers:
                receivers = [receiver.strip() for receiver in receivers.split(',')]
            else:
                receivers = [receivers]

        try:
            server = smtplib.SMTP_SSL(self.host, self.port) if self.ssl else smtplib.SMTP(self.host, self.port)
            server.login(self.user, self.password)
            server.sendmail(self.user, receivers, msg.as_string())
            logging.info("Send email to %s done!" % ','.join(receivers))
        except Exception as ex:
            logging.exception(ex)


email = Email()
