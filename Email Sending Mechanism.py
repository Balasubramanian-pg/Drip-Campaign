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
