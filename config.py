# config.py

# MongoDB configurations
MONGODB_CONNECTION_STRING = ''
MONGODB_DB_NAME = 'master'
MONGODB_COLLECTIONS = ['billboard', 'static_billboard']


GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.compose"
GOOGLE_SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
GOOGLE_DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]
GOOGLE_CLIENT_SECRETS_FILE_SHEETS = "/home/mohamed-fazan2/MW/reverse_geo_coding/.apps.googleusercontent.com.json"
GOOGLE_CLIENT_SECRETS_FILE_DRIVE = "/home/mohamed-fazan2/MW/reverse_geo_coding/.apps.googleusercontent.com.json"
GOOGLE_CLIENT_SECRETS_FILE_MAIL= "/home/mohamed-fazan2/MW/reverse_geo_coding/c.apps.googleusercontent.com.json"

SENDER_EMAIL = ""
RECEIVER_EMAIL = ""
CC_EMAIL = ""
EMAIL_SUBJECT = "Reverse Geocoding of Invalid Coordinates for Newly Onboarded Sites"
EMAIL_MESSAGE = (
    "Hi Team,\n\n"
    "I hope this email finds you well.\n\n"
    "Please find attached the reverse geocoding of invalid coordinates for the newly onboarded sites. Kindly validate and take the necessary actions.\n\n"
    "Best regards,\n"
    " "
)


# GOOGLE_SHEET_CREDENTIALS_FILE = "sheet_token.json"
GOOGLE_SHEET_TOKEN_FILE = "sheet_token.json"
GOOGLE_MAIL_TOKEN_FILE = "token.json"
GOOGLE_DRIVE_TOKEN_FILE = "drive_token.json"
MAPBOX_ACCESS_TOKEN= ""
