from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES_SPREAD_READ = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def get_creds(scopes, token_file='token.json', credentials_file='credentials.json', **kwargs):
    """
    Credit: https://developers.google.com/sheets/api/quickstart/python
    :param scopes google scopes
    :param token_file token file to reuse
    :param credentials_file should be make and given
    :param kwargs:
    :return:
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds


def read_spreadsheet(sid, srange, **kwargs):
    """
    read spreadsheet with sid and srange given
    return array of array
    """
    creds = get_creds(scopes=SCOPES_SPREAD_READ, **kwargs)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sid, range=srange).execute()
    values = result.get('values', [])

    if not values:
        return None
    else:
        return [row for row in values]
