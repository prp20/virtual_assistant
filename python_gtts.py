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

SCOPES = ['https://www.googleapis.com/auth/calendar']
API_KEY = config("WEATHER_API_KEY")
retry=0
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
    return data

def respond(audioString):
    tts = gTTS(text=audioString, lang='en')
    tts.save("speech.mp3")
    playsound.playsound("speech.mp3")

def digital_assistant(data):
    global retry
    print("In digital assistant \n")
    if "how are you" in data:
        listening = True
        respond("I am well")

    elif "time" in data:
        listening = True
        respond(ctime())
        
    elif "weather" in data:
        report = weather_report()
        listening = True
        respond(report)

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



# time.sleep(2)
# respond("Hi Prasad, how can I help you? Please tell me")
# listening = True
# while listening == True and retry < 3:
#     data = listen()
#     listening = digital_assistant(data)
# digital_assistant("thank you")


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

def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f'Getting the upcoming {n}events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=n, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

service = authenticate_google()
get_events(2,service)