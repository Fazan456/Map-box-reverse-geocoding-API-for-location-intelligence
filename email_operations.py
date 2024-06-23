import os.path
import base64
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from google_sheet_service import get_google_sheet_url, upload_geocoding_dataframe_to_google_sheet
from config import (
    GMAIL_SCOPE,
    GOOGLE_CLIENT_SECRETS_FILE_MAIL,
    GOOGLE_MAIL_TOKEN_FILE,
    GOOGLE_CLIENT_SECRETS_FILE_DRIVE 
)


def create_message(sender, to, cc, subject, message_text, spreadsheet_id):
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    message["cc"] = cc

    sheet_url = get_google_sheet_url(spreadsheet_id)
    message_text += f"\nGoogle Sheet URL: {sheet_url}"

    msg = MIMEText(message_text)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("Message Id: %s" % message["id"])
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_gmail_service():
    creds = None
    if os.path.exists(GOOGLE_MAIL_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GOOGLE_MAIL_TOKEN_FILE, GMAIL_SCOPE)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CLIENT_SECRETS_FILE_MAIL,
                GMAIL_SCOPE,
            )
            creds = flow.run_local_server(port=0)
        with open(GOOGLE_MAIL_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email_with_google_sheet_url(sender_email, receiver_email, cc_email, subject, message_text, spreadsheet_id):
    gmail_service = get_gmail_service()
    message = create_message(sender_email, receiver_email, cc_email, subject, message_text, spreadsheet_id)
    send_message(gmail_service, "me", message)
    print("Email Sent Successfully!")

# Example usage within the main script
