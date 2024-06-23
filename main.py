import asyncio
from datetime import datetime
import pandas as pd
from mongodb_operations import get_newly_onboarded_sites
from email_operations import send_email_with_google_sheet_url
from google_sheet_service import  upload_geocoding_dataframe_to_google_sheet
from geocoding import get_geocoding_results
import config

def main():
    # Get duplicate reference IDs and upload to Google Sheets
    aggregation_results = get_newly_onboarded_sites()
    # spreadsheet_url_aggregation = upload_dataframe_to_google_sheet(aggregation_results)

    # Run the geocoding and upload to Google Sheets
    geocoding_df = asyncio.run(get_geocoding_results())
    spreadsheet_url_geocoding = upload_geocoding_dataframe_to_google_sheet(geocoding_df)

    sender_email = config.SENDER_EMAIL
    receiver_email = config.RECEIVER_EMAIL
    cc_email = config.CC_EMAIL

    today_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"{config.EMAIL_SUBJECT} on {today_date}"

    message_text = config.EMAIL_MESSAGE

    if spreadsheet_url_geocoding:
        spreadsheet_id_aggregation = spreadsheet_url_geocoding.split('/')[-1]
        send_email_with_google_sheet_url(sender_email, receiver_email, cc_email, subject, message_text, spreadsheet_id_aggregation)
    else:
        print("Failed to upload aggregation data to Google Sheets.")

    if spreadsheet_url_geocoding:
        spreadsheet_id_geocoding = spreadsheet_url_geocoding.split('/')[-1]
        send_email_with_google_sheet_url(sender_email, receiver_email, cc_email, subject, message_text, spreadsheet_id_geocoding)
    else:
        print("Failed to upload geocoding data to Google Sheets.")

if __name__ == "__main__":
    main()
