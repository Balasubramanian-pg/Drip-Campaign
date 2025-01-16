# contact_manager.py
import pandas as pd
import re
from datetime import datetime, timedelta

class ContactManager:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.df = None
        self.load_contacts()

    def load_contacts(self):
        self.df = pd.read_excel(self.excel_file)
        self._initialize_columns()
        self._process_names()

    def _initialize_columns(self):
        for col in ['Status', 'First_Name', 'Next_Scheduled']:
            if col not in self.df.columns:
                self.df[col] = ''

    def _process_names(self):
        self.df['First_Name'] = self.df.apply(self._extract_name_or_company, axis=1)

    def _extract_name_or_company(self, row):
        if 'Name' in row and pd.notna(row['Name']):
            name = re.sub(r'\d+', '', str(row['Name'])).strip()
            first_name = name.split()[0] if name else None
            
            if first_name and re.match(r'^[a-zA-Z]+$', first_name):
                return first_name
        
        email = str(row['Email']).lower()
        company = email.split('@')[1].split('.')[0]
        return company.capitalize()

    def save_status(self, index, status, next_scheduled):
        self.df.at[index, 'Status'] = status
        self.df.at[index, 'Next_Scheduled'] = next_scheduled
        self.df.to_excel(self.excel_file, index=False)

    def get_contacts_for_round(self, round_num):
        if round_num == 1:
            return self.df[pd.isna(self.df['Status'])]
        return self.df[self.df['Status'].str.contains(f'Round {round_num - 1} sent', na=False)]