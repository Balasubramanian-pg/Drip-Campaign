# main.py
import logging
from config import LOGGING_CONFIG
from campaign_manager import CampaignManager

def setup_logging():
    logging.basicConfig(**LOGGING_CONFIG)

def main():
    setup_logging()
    campaign = CampaignManager()
    campaign.run()

if __name__ == "__main__":
    main()