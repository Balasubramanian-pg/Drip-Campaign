# Drip-Campaign
# Email Campaign Manager

This project is an Email Campaign Manager that automates sending a series of emails to a list of contacts. The project is designed to send initial and follow-up emails based on a specified schedule. 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Email Sending**: Send initial and follow-up emails based on a configurable schedule.
- **Excel Integration**: Load contact list from an Excel file.
- **Logging**: Log email sending status and errors.
- **Configurable Email Templates**: Customize email templates for different rounds of emails.
- **Error Handling**: Robust error handling for email sending failures.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/email-campaign-manager.git
    cd email-campaign-manager
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **SMTP Configuration**: Update the `config.py` file with your SMTP server details and sender email credentials.
    ```python
    SMTP_CONFIG = {
        "SERVER": "smtp-mail.outlook.com",
        "PORT": 587,
        "SENDER_EMAIL": "deepakvk@flipcarbon.com",
        "SENDER_PASSWORD": "your_password"  # Use environment variables for sensitive data
    }
    ```

2. **Logging Configuration**: Configure logging settings in `config.py`.
    ```python
    LOGGING_CONFIG = {
        "filename": 'email_campaign.log',
        "level": "INFO",
        "format": '%(asctime)s - %(message)s',
        "datefmt": '%Y-%m-%d %H:%M:%S'
    }
    ```

3. **Campaign Settings**: Update the campaign settings in `config.py`.
    ```python
    CAMPAIGN_CONFIG = {
        "DAYS_BETWEEN_EMAILS": [3, 5, 7],
        "EXCEL_FILE": r"F:/Flipcarbon/SNOV Emails/Test.xlsx",
        "EMAIL_DELAY_RANGE": (30, 90)  # seconds
    }
    ```

4. **Email Templates**: Customize your email templates in `config.py`.
    ```python
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
    ```

## Usage

1. **Run the Campaign**: Execute the main script to start the email campaign.
    ```bash
    python main.py
    ```

2. The campaign will:
    - Load the contact list from the specified Excel file.
    - Send initial emails to contacts who haven't received any emails yet.
    - Schedule and send follow-up emails based on the specified intervals.

## Logging

- The application logs its activities in `email_campaign.log`.
- Logs include information about sent emails, scheduled emails, and any errors encountered.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.
