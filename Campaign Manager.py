# campaign_manager.py
import logging
import time
import random
from datetime import datetime
from config import CAMPAIGN_CONFIG, EMAIL_TEMPLATES
from email_service import EmailService
from contact_manager import ContactManager

class CampaignManager:
    def __init__(self):
        self.email_service = EmailService()
        self.contact_manager = ContactManager(CAMPAIGN_CONFIG["EXCEL_FILE"])
        self.config = CAMPAIGN_CONFIG

    def get_next_schedule_time(self, current_round, current_time):
        if current_round <= len(self.config["DAYS_BETWEEN_EMAILS"]):
            days_to_add = self.config["DAYS_BETWEEN_EMAILS"][current_round - 1]
            next_time = current_time + timedelta(days=days_to_add)
            return next_time.strftime("%d-%m-%y at %I:%M %p")
        return "Not scheduled"

    def process_round(self, round_num):
        current_time = datetime.now()
        contacts = self.contact_manager.get_contacts_for_round(round_num)
        
        for index, row in contacts.iterrows():
            name = row['First_Name']
            scheduled_time = current_time.strftime("%I:%M %p")
            logging.info(f"Email {round_num} scheduled to {name} at {scheduled_time}")
            
            if self.email_service.send_email(
                row['Email'],
                f"{'First Email' if round_num == 1 else f'Follow-up Email {round_num}'} Subject",
                EMAIL_TEMPLATES[round_num].format(name=name)
            ):
                next_schedule = self.get_next_schedule_time(round_num, current_time)
                self.contact_manager.save_status(
                    index,
                    f'Round {round_num} sent at {scheduled_time}',
                    f'Round {round_num + 1} scheduled for {next_schedule}'
                )
                
            time.sleep(random.randint(*self.config["EMAIL_DELAY_RANGE"]))

    def run(self):
        try:
            # First round
            logging.info("Starting first round of emails...")
            self.process_round(1)
            
            # Follow-up rounds
            for round_num in range(2, len(EMAIL_TEMPLATES) + 1):
                wait_days = self.config["DAYS_BETWEEN_EMAILS"][round_num - 2]
                logging.info(f"Waiting {wait_days} days before round {round_num}...")
                time.sleep(wait_days * 86400)
                
                logging.info(f"Starting round {round_num}...")
                self.process_round(round_num)
            
            logging.info("Campaign completed successfully")
            
        except Exception as e:
            logging.error(f"Campaign error: {str(e)}")