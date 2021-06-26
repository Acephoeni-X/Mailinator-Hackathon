from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.shortcuts import render

# Create your views here.

def index(requests):
    messages = main()
    return render(requests, 'index.html', {'message':messages})


def main():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

    ids = service.users().messages().list(userId='me', labelIds='SENT').execute(), service
    all_id = []

    for i in ids:
        all_id.append(i)

    result = []
    for i in all_id[0]['messages']:
        # print(i['id'])
        if ((service.users().messages().get(userId='me', id=i['id']).execute())['snippet'])!='':
            result.append((service.users().messages().get(userId='me', id=i['id']).execute())['snippet'])
    
    return result