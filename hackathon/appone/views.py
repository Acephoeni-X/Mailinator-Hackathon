from __future__ import print_function
import datetime
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
from pickle import dump
from socket import send_fds
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.shortcuts import render
from django.http import HttpResponse
from appone import input
import base64 
from . import sendmail

# Create your views here.

def getUserProfile():
    service = service_return()
    return (service.users().getProfile(userId='me').execute())['emailAddress']

def write_json(data, filename='data.json'):
    with open (filename, 'w+') as f:
        json.dump(data, f, indent=4)

def createJSON(userMail, to_email, message, subject, time, day):
    jsON = {
                "sender": userMail, 
                "to": to_email,
                "message": message,
                "subject": subject,
                "time":time,
                "day" : day
            }
    with open ('data.json') as json_file:
        data = json.load(json_file)
        temp = data['datas']
        temp.append(jsON)
    write_json(data)


def email(requests):
    name = input.sendMail()
    if requests.method == 'POST':
        form = input.sendMail(requests.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            hour = form.cleaned_data['hr']
            mint = form.cleaned_data['mint']
            sec = form.cleaned_data['sec']
            day = requests.POST['value']
            time = f'{hour}:{mint}:{sec}'
            userMail = getUserProfile()
            sendmail.sendMail(to_email, subject, message)
            createJSON(userMail, to_email, message, subject, time, day)
            os.rename('token_gmail_v1.pickle', f'{userMail}.pickle')
            return HttpResponse('DONE')

    return render(requests, 'send_email.html', {'form':name})

def front(requests):
    return render(requests, 'front.html')

def index(requests):
    messages = main()
    return render(requests, 'index.html', {'message':messages})

def service_return():
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
            service = build('gmail', 'v1', credentials=creds)
        username = (service.users().getProfile(userId='me').execute())['emailAddress']
        with open(f'Tokens/{username}.json', 'w') as token:
            token.write(creds.to_json())

    return service

def main():
    service = service_return()
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
        if ((service.users().messages().get(userId='me', id=i['id']).execute())['snippet'])!='':
            result.append((service.users().messages().get(userId='me', id=i['id']).execute())['snippet'])
    return result
