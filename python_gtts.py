from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import requests, json
import playsound
from decouple import config
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
API_KEY = config("WEATHER_API_KEY")
retry=0
MONTHS=["Jaunary", "february", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "Saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        respond("I'm sorry. I could'n get you. Can you please repeat?")
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        respond("I'm sorry. I could'n get you. Can you please repeat?")
        print("Request Failed; {0}".format(e))
    except Exception as e:
        respond("I'm sorry. I could'n get you. Can you please repeat?")
        print(f"Exception: {e}")
    
    return data.lower()

def respond(audioString):
    tts = gTTS(text=audioString, lang='en')
    tts.save("speech.mp3")
    playsound.playsound("speech.mp3")

def digital_assistant(data):
    global retry
    print("In digital assistant \n")
    if "how are you" in data:
        listening = True
        respond("Thank you. I feel wonderful and well. Hope you feel the same.")

    elif "time" in data:
        listening = True
        respond(ctime())
        
    elif "weather" in data:
        report = weather_report()
        listening = True
        respond(report)

    elif "event" in data or "tasks" in data or "plan" in data:
        SERVICE = authenticate_google()
        date = get_date(data)
        if date:
            get_events(date, SERVICE)
        else:
            respond("Please Try Again")
        listening = True

    elif "thank you" in data:
        respond("Thank you. Wake me if you need any help. Have a good day. Byeeeee")
        listening = False
        print('Listening stopped')
        return listening
    else:
        respond("I'm sorry. I could'n get you. Can you please repeat?")
        listening = True
        retry=retry+1

    return listening

def weather_report():
    global API_KEY
    city = "Bangalore"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={str(API_KEY)}&units=metric"
    js = requests.get(weather_url).json()
    if js["cod"] != "404":
        weather = js["main"]
        current_temp = weather["temp"]
        max_temp = weather["temp_max"]
        min_temp = weather["temp_min"]
        humidity = weather["humidity"]
        weather_description = js["weather"][0]["description"]
        report = f"The Current weather in {city} is {weather_description} with current temperature {current_temp} degree celcius and humidity is {humidity}. The maximum temperature can go upto {max_temp} degree celcius and minimum temperature can go upto {min_temp} degree celcius."
        print(report)
    else:
        report= f"Sorry, but I couldn't find the weather report for {city}."
    return(report)

def get_date(text):
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

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

        return today + datetime.timedelta(dif)
    return datetime.date(month=month, day=day, year=year)


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day, service):
    # Call the Calendar API
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
        respond('No upcoming events found.')
    else:
        respond(f'You have a total of {len(events)} events on this day.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            respond(event["summary"] + " at " + start_time)


# time.sleep(2)
respond("Hi Prasad, how can I help you? Please tell me")
listening = True
while listening == True and retry < 3:
    data = listen()
    listening = digital_assistant(data)
if listening:
    digital_assistant("thank you")
