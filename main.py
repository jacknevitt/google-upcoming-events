#!/bin/env python

from __future__ import print_function
import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CALENDAR_ID = 'primary'


def prettyfy_json(json_object):
    return json.dumps(json_object, indent=4, sort_keys=True)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat(
    ) + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 Tech Team Events')
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    # print("EntireJsonBlob::", prettyfy_json(events_result))

    if not events:
        print('No upcoming events found.')
    for event in events:
        location = event.get('location', 'not-set')
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(
            "Event :: {}, Location :: {}, Start time :: {}, End time :: {}, Click here for details :: {}"
            .format(
                event['summary'],
                location,
                start,
                end,
                event['htmlLink'],
            ))


if __name__ == '__main__':
    main()
