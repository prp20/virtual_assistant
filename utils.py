from __future__ import print_function

import datetime, os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from gtts import gTTS
import playsound
import pytz

MONTHS=["jaunary", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "Saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]


def respond(audioString):
    tts = gTTS(text=audioString, lang='en')
    tts.save("speech.mp3")
    playsound.playsound("speech.mp3")

def get_authenticated_google_service(api_name, api_version, scopes):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    print(scopes)
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    print("calling google auth service")
    service = build(api_name, api_version, credentials=creds)
    return service

def convert_to_RFC_datetime(date):
    dt = date.isoformat() + 'Z'
    return dt

def convert_to_local_time(isoTime):
    utctime = datetime.datetime.fromisoformat(isoTime.split("Z")[0])
    return utctime

def get_date(text, time=None):
    result_date = None
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    # _, week_num, day_of_week = my_date.isocalendar()
    if text.count("today") > 0:
        result_date= today
    elif text.count("yesterday") > 0:
        result_date= yesterday
    elif text.count("tomorrow") > 0:
        result_date= tomorrow
    
    if result_date == None:
        day = -1
        day_of_the_week = -1
        month = -1
        year = today.year

        for word in text.split():
            if word in MONTHS:

                month = MONTHS.index(word) + 1
            elif word in DAYS:
                day_of_the_week = DAYS.index(word)
            elif word.isdigit():
                day = int(word)
            else:
                for ext in DAY_EXTENSIONS:
                    found = word.find(ext)
                    if found > 0:
                        try:
                            day = int(word[:found])
                        except:
                            pass
        if month < today.month and month != -1:
            year = year + 1

        if day < today.day and month == -1  and day != -1:
            month = month +1

        if month == -1 and day == -1 and day_of_the_week != -1:
            current_day_of_the_week = today.weekday()
            dif = day_of_the_week - current_day_of_the_week
            if dif < 0:
                dif += 7
                if text.count("next") >= 1:
                    dif += 7

            result_date= today + datetime.timedelta(dif)
        result_date= datetime.date(month=month, day=day, year=year)

    if time == None:
        result_date = datetime.datetime.combine(result_date, datetime.datetime.max.time())
    else:
        print(time)
        ampm = ["PM" if time.split(" ")[-1].split(".")[0] == 'p' else "AM" ][0]
        print(ampm)
        res_time = f"{time.split(' ')[1]} {ampm}"
        print(res_time)
        format = ' %I:%M %p'
        datetime_str = datetime.datetime.strptime(date_time, format)

    return result_date