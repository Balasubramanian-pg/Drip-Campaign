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
