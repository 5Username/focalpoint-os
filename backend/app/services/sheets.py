"""
Google Sheets integration for Incident sync.

Setup:
1. Create a Google Cloud project + enable Google Sheets API
2. Create a Service Account and download JSON key
3. Share the target Sheet with the service account email
4. Set GOOGLE_SHEETS_CREDENTIALS_FILE and SPREADSHEET_ID in .env
"""

from typing import Dict, Any, Optional
import os

# Placeholder implementation — replace with real google-api-python-client calls

def append_incident(row: Dict[str, Any], spreadsheet_id: Optional[str] = None) -> bool:
    """
    Append an incident row to the configured Google Sheet.
    Returns True on success.
    """
    spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
    creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")

    if not spreadsheet_id or not creds_file:
        print("[sheets] Missing SPREADSHEET_ID or credentials — running in dry-run mode")
        print("[sheets] Would append:", row)
        return True

    # Real implementation would look like:
    # from google.oauth2 import service_account
    # from googleapiclient.discovery import build
    # creds = service_account.Credentials.from_service_account_file(creds_file)
    # service = build('sheets', 'v4', credentials=creds)
    # values = [[row.get('id'), row.get('title'), ...]]
    # service.spreadsheets().values().append(...).execute()

    return True
