import os
import pickle
import base64
import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

TOKEN_FILENAME = 'token.pickle'


###
# Enable the Drive API and download your credentials file here:
# https://developers.google.com/drive/api/v3/quickstart/python
###


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILENAME):
        with open(TOKEN_FILENAME, 'rb') as token:
            creds = pickle.load(token)

    if os.environ.get('GOOGLE_API_CREDS'):
        creds_base64 = base64.b64decode(os.environ.get('GOOGLE_API_CREDS'))
        service_creds = json.loads(creds_base64)

        creds = service_account.Credentials.from_service_account_info(
            service_creds, scopes=SCOPES
        )
        return creds

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILENAME, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_spreadsheets():
    service = build('sheets', 'v4', credentials=get_creds())
    return service.spreadsheets()
