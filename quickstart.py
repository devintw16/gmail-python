#! /usr/local/bin/python3
from __future__ import print_function
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getCreds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    print("about to look for")
    if os.path.exists('token.json'):
        print("no token.json found")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return creds

def getLabels():
    service = build('gmail', 'v1', credentials=getCreds())

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def getMessagesIds():
    service = build('gmail', 'v1', credentials=getCreds())
    nextPageToken = ''
    messages = []
    while True:
        result = service.users().messages().list(userId='me',labelIds='INBOX', maxResults=500, pageToken=nextPageToken).execute()
        if 'nextPageToken' in result:
            nextPageToken = result['nextPageToken']
            print("nextPageToken found: {0} ".format(nextPageToken))
            messages.extend(result['messages'])
            print ("Total messages in inbox: ", str(len(messages)))
        else:
            messages.extend(result['messages'])
            print ("Total messages in inbox: ", str(len(messages)))
            break

    return messages

if __name__ == '__main__':
    getLabels()
    messages_ids = getMessageIds()
    

