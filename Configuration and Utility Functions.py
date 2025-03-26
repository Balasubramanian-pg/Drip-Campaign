import os
import random
import pandas as pd
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime, timedelta

# Configuration Class
class EmailCampaignConfig:
    def __init__(self, 
                 sender_email, 
                 sender_password, 
                 input_excel_path, 
                 log_file_path='email_campaign_log.txt'):
        """
        Initialize configuration for the email campaign
        
        :param sender_email: Gmail email address to send from
        :param sender_password: App password for Gmail account
        :param input_excel_path: Path to the input Excel file
        :param log_file_path: Path to log file for tracking operations
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.input_excel_path = input_excel_path
        self.log_file_path = log_file_path
        
        # Load the input Excel file
        self.df = pd.read_excel(input_excel_path)
        
        # Ensure required columns exist
        required_columns = [
            'First Name', 
            'Email Address', 
            'Email Sent Status', 
            'Response Status', 
            'Follow-up Status'
        ]
        for col in required_columns:
            if col not in self.df.columns:
                self.df[col] = ''
        
    def log_event(self, message):
        """
        Log events to a file with timestamp
        
        :param message: Event message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"[{timestamp}] {message}\n")
        
    def save_dataframe(self):
        """
        Save updated DataFrame back to Excel
        """
        self.df.to_excel(self.input_excel_path, index=False)

# Utility Functions
def generate_personalized_email(first_name):
    """
    Generate a personalized email template
    
    :param first_name: Recipient's first name
    :return: Email body as string
    """
    email_template = f"""
    Dear {first_name},

    I hope this email finds you well. I wanted to reach out and discuss...

    [Personalized content goes here]

    Best regards,
    [Your Name]
    """
    return email_template.strip()

def get_random_delay():
    """
    Generate a random delay between email sends to avoid spam detection
    
    :return: Random delay in seconds
    """
    return random.uniform(30, 180)  # 30 to 180 seconds delay
