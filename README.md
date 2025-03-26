# Drip-Campaign

# Automated Email Campaign System

## Project Overview

An automated Python-based system for managing email campaigns, tracking responses, and sending follow-up emails.

## Features

- Personalized email sending
- Automated response tracking
- Follow-up email mechanism
- Detailed logging and reporting

## Prerequisites

- Python 3.7+
- pip

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install pandas schedule
   ```

## Configuration

### Gmail Setup
1. Enable 2-Step Verification
2. Generate an App Password

### Excel Spreadsheet
Create an Excel file with columns:
- First Name
- Email Address
- Email Sent Status
- Response Status
- Follow-up Status

## Usage

1. Update script configuration with:
   - Gmail credentials
   - Excel file path

2. Run the script:
   ```
   python email_campaign.py
   ```

## Project Structure

- `email_campaign.py`: Main script
- `campaign_contacts.xlsx`: Contact database
- Logging files generated during execution

## Limitations

- Gmail account only
- Requires continuous script execution
- Subject to Gmail sending quotas

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Create pull request
