from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
import smtplib

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'kunbun@mail.com'
SENDER_PASSWORD = 'KUNBUN@1025'

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From']= SENDER_ADDRESS
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))
    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


