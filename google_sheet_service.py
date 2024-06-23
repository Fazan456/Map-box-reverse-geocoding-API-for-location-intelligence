import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pandas as pd
from datetime import datetime
import config

def get_credentials_sheets():
    credentials = None
    if os.path.exists(config.GOOGLE_SHEET_TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(config.GOOGLE_SHEET_TOKEN_FILE, config.GOOGLE_SHEETS_SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(config.GOOGLE_CLIENT_SECRETS_FILE_SHEETS, config.GOOGLE_SHEETS_SCOPES)
            credentials = flow.run_local_server(port=0)
    
    return credentials

def create_spreadsheet(credentials):
    service = build("sheets", "v4", credentials=credentials)
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    spreadsheet_title = f"Geocoding Results on {today_date}"
    
    spreadsheet = {
        'properties': {
            'title': spreadsheet_title
        }
    }
    
    try:
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')
    except Exception as e:
        print(f"An error occurred while creating the spreadsheet: {e}")
        return None

def get_sheet_service(credentials):
    return build("sheets", "v4", credentials=credentials)

def get_google_sheet_url(spreadsheet_id):
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"

def upload_geocoding_dataframe_to_google_sheet(geocoding_df):
    credentials = get_credentials_sheets()
    sheet_service = get_sheet_service(credentials)
    spreadsheet_id = create_spreadsheet(credentials)
    
    if spreadsheet_id:
        # Check if 'Geocoding Results' sheet exists and get its sheetId
        existing_sheets = sheet_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()['sheets']
        sheet_id = None
        
        for sheet in existing_sheets:
            if sheet['properties']['title'] == 'Geocoding Results':
                sheet_id = sheet['properties']['sheetId']
                break
        
        if not sheet_id:
            # Create 'Geocoding Results' sheet if it doesn't exist
            new_sheet_request = {
                'requests': [
                    {
                        'addSheet': {
                            'properties': {
                                'title': 'Geocoding Results'
                            }
                        }
                    }
                ]
            }
            
            try:
                sheet_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=new_sheet_request).execute()
                print(f"Created new sheet 'Geocoding Results' in the spreadsheet ID: {spreadsheet_id}")
            except Exception as e:
                print(f"An error occurred while creating 'Geocoding Results' sheet: {e}")
                return None
        
        # Clean up and prepare data for upload
        # geocoding_df_clean = geocoding_df.fillna('')  # Replace NaN values with empty string
        
        # Convert all values to strings to ensure proper formatting
        geocoding_df_clean = geocoding_df.astype(str)
    
        
        # Upload dataframe to the 'Geocoding Results' sheet
        values = [geocoding_df_clean.columns.values.tolist()] + geocoding_df_clean.values.tolist()
        value_range = "Geocoding Results!A1"  # Update to the correct sheet and range if necessary
        value_input_option = 'RAW'
        body = {'values': values}
        
        try:
            request = sheet_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=value_range,
                valueInputOption=value_input_option,
                body=body
            )
            request.execute()
            
            print(f"Dataframe uploaded to the Google Sheet 'Geocoding Results' in the Spreadsheet ID '{spreadsheet_id}'.")
            sheet_url = get_google_sheet_url(spreadsheet_id)
            return sheet_url
        
        except Exception as e:
            print(f"An error occurred while uploading dataframe to 'Geocoding Results': {e}")
            return None
        
    else:
        print("Failed to create the spreadsheet.")
        return None
