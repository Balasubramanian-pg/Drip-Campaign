# email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_CONFIG
import logging

class EmailService:
    def __init__(self):
        self.smtp_config = SMTP_CONFIG

    def connect(self):
        self.server = smtplib.SMTP(self.smtp_config["SERVER"], self.smtp_config["PORT"])
        self.server.starttls()
        self.server.login(self.smtp_config["SENDER_EMAIL"], self.smtp_config["SENDER_PASSWORD"])

    def disconnect(self):
        if hasattr(self, 'server'):
            self.server.quit()

    def send_email(self, recipient, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config["SENDER_EMAIL"]
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            self.connect()
            self.server.send_message(msg)
            self.disconnect()
            
            logging.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {str(e)}")
            return False