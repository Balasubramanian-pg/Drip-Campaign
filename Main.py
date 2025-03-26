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
