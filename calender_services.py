from __future__ import print_function

import datetime, os.path
import utils
import pytz
import utils
# If modifying these scopes, delete the file token.json.
MONTHS=["jaunary", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "Saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]

event = {
  'summary': '',
  'location': '',
  'description': '',
  'start': {
    'dateTime': '',
    'timeZone': 'Asia/Kolkata',
  },
  'end': {
    'dateTime': '',
    'timeZone': 'Asia/Kolkata',
  }
}

def get_events(day, creds):
    # Call the Calendar API
    service = utils.get_authenticated_google_service('calendar', 'v3', ['https://www.googleapis.com/auth/calendar'])
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end = end.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        utils.respond('No upcoming events found.')
    else:
        utils.respond(f'You have a total of {len(events)} events on this day.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"
            utils.respond(event["summary"] + " at " + start_time)

def create_google_event(summary,starttime, endtime, description=None, location=None, service=None):
    event["summary"] = summary
    event["start"]["datetime"] = starttime
    event["end"]["datetime"] = endtime
    event["description"] = description
    event["location"] = location
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



def calender_services():
    credentials = utils.authenticate_google()
    get_events(credentials)
