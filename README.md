# Drip-Campaign

I'll help you create a Python implementation for the Automated Email Campaign and Follow-up System. I'll break this down into multiple artifacts to make the code more manageable and organized.

Let's start with the main components:

```python
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

```

```python
import smtplib
from email.mime.text import MIMEText
import time
import random

class EmailSender:
    def __init__(self, config):
        """
        Initialize EmailSender with campaign configuration
        
        :param config: EmailCampaignConfig object
        """
        self.config = config
    
    def send_email(self, recipient_email, subject, body):
        """
        Send an email using Gmail SMTP
        
        :param recipient_email: Recipient's email address
        :param subject: Email subject
        :param body: Email body
        :return: Boolean indicating send success
        """
        try:
            # Create MIME message
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.config.sender_email
            msg['To'] = recipient_email
            
            # Establish secure SMTP connection
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.config.sender_email, self.config.sender_password)
                server.send_message(msg)
            
            # Log successful send
            self.config.log_event(f"Email sent to {recipient_email}")
            return True
        
        except Exception as e:
            # Log send failure
            self.config.log_event(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
    
    def send_campaign_batch(self):
        """
        Send emails in batches with random delays
        """
        # Find unsent emails
        unsent_emails = self.config.df[self.config.df['Email Sent Status'] != 'Yes']
        
        for index, row in unsent_emails.iterrows():
            # Personalize email
            email_body = generate_personalized_email(row['First Name'])
            
            # Send email
            send_success = self.send_email(
                recipient_email=row['Email Address'],
                subject='Personalized Campaign Outreach',
                body=email_body
            )
            
            # Update Excel sheet
            if send_success:
                self.config.df.at[index, 'Email Sent Status'] = 'Yes'
                
                # Random delay to avoid spam detection
                delay = get_random_delay()
                time.sleep(delay)
        
        # Save updated DataFrame
        self.config.save_dataframe()

```

```python
import imaplib
import email
from datetime import datetime, timedelta

class ResponseMonitor:
    def __init__(self, config):
        """
        Initialize ResponseMonitor with campaign configuration
        
        :param config: EmailCampaignConfig object
        """
        self.config = config
        self.email_sender = EmailSender(config)
    
    def check_inbox_responses(self):
        """
        Check Gmail inbox for responses to sent emails
        """
        try:
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.config.sender_email, self.config.sender_password)
            mail.select('inbox')
            
            # Find sent emails waiting for response
            sent_emails = self.config.df[
                (self.config.df['Email Sent Status'] == 'Yes') & 
                (self.config.df['Response Status'] != 'Received')
            ]
            
            for index, row in sent_emails.iterrows():
                # Search for emails from this recipient
                search_criteria = f'(FROM "{row["Email Address"]}")'
                _, message_numbers = mail.search(None, search_criteria)
                
                if message_numbers[0]:
                    # Mark as responded
                    self.config.df.at[index, 'Response Status'] = 'Received'
                    self.config.log_event(f"Response received from {row['Email Address']}")
            
            # Save updates
            self.config.save_dataframe()
            mail.close()
            mail.logout()
        
        except Exception as e:
            self.config.log_event(f"Error checking inbox: {str(e)}")
    
    def send_follow_ups(self):
        """
        Send follow-up emails to non-responders
        """
        # Find emails sent but not responded to
        no_response_emails = self.config.df[
            (self.config.df['Email Sent Status'] == 'Yes') & 
            (self.config.df['Response Status'] != 'Received') &
            (self.config.df['Follow-up Status'] != 'Sent')
        ]
        
        for index, row in no_response_emails.iterrows():
            follow_up_body = f"""
            Dear {row['First Name']},

            I'm following up on my previous email. I wanted to ensure you received my initial message.

            [Follow-up content]

            Best regards,
            [Your Name]
            """
            
            send_success = self.email_sender.send_email(
                recipient_email=row['Email Address'],
                subject='Quick Follow-up',
                body=follow_up_body
            )
            
            if send_success:
                self.config.df.at[index, 'Follow-up Status'] = 'Sent'
                time.sleep(get_random_delay())
        
        # Save updates
        self.config.save_dataframe()

```

```python
import schedule
import time

class EmailCampaignRunner:
    def __init__(self, config):
        """
        Initialize campaign runner with configuration
        
        :param config: EmailCampaignConfig object
        """
        self.config = config
        self.email_sender = EmailSender(config)
        self.response_monitor = ResponseMonitor(config)
    
    def run_daily_campaign(self):
        """
        Run daily email campaign tasks
        """
        try:
            # Send email batch
            self.email_sender.send_campaign_batch()
            
            # Check inbox for responses
            self.response_monitor.check_inbox_responses()
            
            # Send follow-ups if needed
            self.response_monitor.send_follow_ups()
            
            # Generate daily report
            self.generate_daily_report()
        
        except Exception as e:
            self.config.log_event(f"Daily campaign error: {str(e)}")
    
    def generate_daily_report(self):
        """
        Generate a consolidated daily report
        """
        today = datetime.now().strftime("%Y-%m-%d")
        report_filename = f"campaign_report_{today}.txt"
        
        with open(report_filename, 'w') as report_file:
            report_file.write(f"Daily Campaign Report - {today}\n\n")
            
            # Responses received today
            responses = self.config.df[self.config.df['Response Status'] == 'Received']
            report_file.write(f"Total Responses: {len(responses)}\n\n")
            
            for index, row in responses.iterrows():
                report_file.write(f"Recipient: {row['First Name']} ({row['Email Address']})\n")
        
        self.config.log_event(f"Daily report generated: {report_filename}")
    
    def start_campaign(self):
        """
        Schedule and start the email campaign
        """
        # Schedule daily tasks
        schedule.every().day.at("09:00").do(self.run_daily_campaign)
        schedule.every().day.at("14:00").do(self.run_daily_campaign)
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)

# Example Usage
def main():
    # Replace with your actual details
    config = EmailCampaignConfig(
        sender_email='your_email@gmail.com',
        sender_password='your_app_password',
        input_excel_path='campaign_contacts.xlsx'
    )
    
    campaign = EmailCampaignRunner(config)
    campaign.start_campaign()

if __name__ == "__main__":
    main()

```

I've created a comprehensive Python implementation of the Automated Email Campaign and Follow-up System based on the requirement gathering document. Let me break down the key components:

1. `EmailCampaignConfig`: 
   - Manages configuration and logging
   - Handles Excel sheet interactions
   - Ensures required columns exist

2. `EmailSender`:
   - Sends personalized emails
   - Implements random delays to avoid spam detection
   - Tracks email sending status

3. `ResponseMonitor`:
   - Checks inbox for responses
   - Tracks response status
   - Sends follow-up emails

4. `EmailCampaignRunner`:
   - Coordinates daily campaign tasks
   - Schedules email sending and monitoring
   - Generates daily reports

Important Notes and Prerequisites:
1. You'll need to use a Gmail App Password, not your regular password
2. Install required libraries: 
   ```
   pip install pandas schedule yagmail
   ```
3. Replace placeholders:
   - `your_email@gmail.com`
   - `your_app_password`
   - `campaign_contacts.xlsx`

4. Create an Excel file with columns:
   - First Name
   - Email Address
   - Email Sent Status
   - Response Status
   - Follow-up Status

Recommendations:
- Enable 2-Factor Authentication on your Gmail
- Generate an App Password specifically for this script
- Be mindful of Gmail's sending limits

Would you like me to elaborate on any part of the implementation or discuss how to set it up?
