# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calander_events_of_the_day(number_of_events):
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
    try:
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

    except Exception as e:
        print('-------------  Error ------------ \n\n', e,
               '\n\n -------------------------------- \n\n')
        print('If you did not turn on your google api yet. Please visit the',
              'the following website:',
              'https://developers.google.com/calendar/quickstart/python',
              'and click on the button enable the google calander API.')
        sys.exit(1)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z'indicates UTC time
    todays_date = datetime.datetime.now().date()

    # The timeslot between 11 and 12 pm will be not considered, because
    # otherwise all-day events of the next day will be displayed as well

    end_of_the_day = datetime.datetime(todays_date.year, todays_date.month,
                                       todays_date.day, 23, 00, 00).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=end_of_the_day,
                                          maxResults=number_of_events,
                                          singleEvents=True,
                                          orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    event_essential_information = []
    for event in events:
        # Get events with a given date or time or all time events
        start = event['start'].get('dateTime', event['start'].get('date'))

        event_essential_information.append({'start_moment': start,
                                            'title': event['summary']})

    return event_essential_information


if __name__ == '__main__':
    get_calander_events_of_the_day(2)

# [END calendar_quickstart]
