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
    path_of_file = os.path.dirname(os.path.abspath(__file__))
    path_to_token_pickle = os.path.join(path_of_file, 'token.pickle')
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path_to_token_pickle):
        with open(path_to_token_pickle , 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                path_tp_credentials = os.path.join(path_of_file,
                                                   'credentials.json')
                flow = InstalledAppFlow.from_client_secrets_file(
                    path_tp_credentials, SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run

            with open(path_to_token_pickle, 'wb') as token:
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
    now = datetime.datetime.utcnow()
    now = now + datetime.timedelta(hours=1) #Add one hour to be in GMT time zone
    now = now.isoformat() + 'Z'  # 'Z'indicates UTC time, I mean not really.
    todays_date = datetime.datetime.now().date()

    # The timeslot between 11 and 12 pm will be not considered, because
    # otherwise all-day events of the next day will be displayed as well

    end_of_the_day = datetime.datetime(todays_date.year, todays_date.month,
                                       todays_date.day, 23, 00, 00).isoformat() + 'Z'

    print(now)
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
        date_time = start.split('T')
        date = date_time[0]

        if len(date_time) > 1:
            time_with_seconds = date_time[1].split('+')[0]
            # format of time_with_seconds is H:M:S, but we only need H:M
            # Use rsplit to split on the last :
            time = time_with_seconds.rsplit(':', maxsplit=1)[0]
        else:
            time = ''
            
        event_essential_information.append({'start_time': time,
                                            'start_date': date,
                                            'title': event['summary']})

    return event_essential_information


if __name__ == '__main__':
    get_calander_events_of_the_day(2)

# [END calendar_quickstart]
