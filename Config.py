# config.py
SMTP_CONFIG = {
    "SERVER": "smtp-mail.outlook.com",
    "PORT": 587,
    "SENDER_EMAIL": "deepakvk@flipcarbon.com",
    "SENDER_PASSWORD": "Flipcfo@08062020"  # Consider using environment variables for sensitive data
}

LOGGING_CONFIG = {
    "filename": 'email_campaign.log',
    "level": "INFO",
    "format": '%(asctime)s - %(message)s',
    "datefmt": '%Y-%m-%d %H:%M:%S'
}

CAMPAIGN_CONFIG = {
    "DAYS_BETWEEN_EMAILS": [3, 5, 7],
    "EXCEL_FILE": r"F:/Flipcarbon/SNOV Emails/Test.xlsx",
    "EMAIL_DELAY_RANGE": (30, 90)  # seconds
}

EMAIL_TEMPLATES = {
    1: """Hello {name},
This is the first email in our campaign.
Best regards,
Your Company""",
    
    2: """Hello {name},
This is the second follow-up email.
Best regards,
Your Company""",
    
    3: """Hello {name},
This is the third follow-up email.
Best regards,
Your Company""",
    
    4: """Hello {name},
This is the final follow-up email.
Best regards,
Your Company"""
}