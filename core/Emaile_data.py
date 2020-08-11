# -*- coding: utf-8 -*-
import smtplib
import email
# Constructing text
from email.mime.text import MIMEText
# Constructing picture
from email.mime.image import MIMEImage
# Collection objects
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.header import make_header

class emaile:
    def __init__(self, sender, license, receiver, subject, attach_file, attach_file2):
        self.sender = sender
        self.license = license
        self.receiver = receiver
        self.subject = subject
        self.attach_file = attach_file
        self.attach_file2 = attach_file2
        
    def send_emaile(self):
        # SMTP Service
        mail_host = "smtp.163.com"
        # Sender's mailbox
        mail_sender = self.sender
        # E-mail authorization code
        mail_license = self.license
        # Recipient mailbox, could be multiple recipients
        mail_receivers = self.receiver

        mm = MIMEMultipart('related')

        # Message subject
        subject_content = self.subject
        # Sender
        mm["From"] = "sender_name" + "<" + self.sender + ">"
        # Accepter
        mm["To"] = "receiver_1_name<" + self.receiver[0] + ">,receiver_2_name<" + self.receiver[1] + ">"
        # Main object
        mm["Subject"] = Header(subject_content,'utf-8')

        # Emaile body
        body_content = """你好，出现异常订单！"""
        # Parameters
        message_text = MIMEText(body_content,"plain","utf-8")
        # Add text
        mm.attach(message_text)


        # Constructing attachments
        atta = MIMEText(open(self.attach_file, 'rb').read(), 'base64', 'utf-8')
        atta["Content-Type"] = 'application/octet-stream; name = "%s"' %make_header([(self.attach_file, 'gbk')]).encode('gbk')
        atta["Content-Disposition"] = 'attachment; filename="%s"' %make_header([(self.attach_file, 'gbk')]).encode('gbk')
        mm.attach(atta)

        atta2 = MIMEText(open(self.attach_file2, 'rb').read(), 'base64', 'utf-8')
        atta2["Content-Type"] = 'application/octet-stream; name = "%s"' %make_header([(self.attach_file2, 'gbk')]).encode('gbk')
        atta2["Content-Disposition"] = 'attachment; filename="%s"' %make_header([(self.attach_file2, 'gbk')]).encode('gbk')
        mm.attach(atta2)

        # Create SMTP object
        stp = smtplib.SMTP()
        # Set the domain name and port of the sender's mailbox, the port address is 25
        stp.connect(mail_host, 25)
        # set_debuglevel(1) could print out all the information interacting with the SMTP server
        stp.set_debuglevel(1)
        # Log in to the mailbox
        stp.login(mail_sender,mail_license)
        # Send mail
        stp.sendmail(mail_sender, mail_receivers, mm.as_string())
        print("邮件发送成功")
        # Close SMTP object
        stp.quit()



