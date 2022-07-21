import pyttsx3 as pyt
import warnings
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import calendar, requests, json
import datetime

warnings.filterwarnings("ignore")

engine = pyt.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', rate-50)
engine.runAndWait()

def speak(data):
    engine.say(data)
    engine.runAndWait()

def hear():
    rec_voice = sr.Recognizer()
    speak("Hello Mr. Prasad, how can I help you today?")
    with sr.Microphone() as source:
        print("Listening.....")
        audio = rec_voice.listen(source)

    data = " "
    try:
        data = rec_voice.recognize_google(audio)
        speak("You said: " + data )

    except sr.UnknownValueError:
        speak("Sorry, I couldn't get you !!!")
    except sr.RequestError as ex:
        speak("Sorry, there was a confusion. Can you please try again")

    return(data)

def response(input_text):
    print(input_text)
    tts = gTTS(test=input_text, lang="en")
    audio = "Audio.mp3"
    tts.save(audio)
    playsound.playsound(audio)
    os.remove(audio)

def call(text):
    action_call = "Sunday"
    text=text.lower()
    return(True if action_call in text else False)


def today_date():
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day
    month_list=["Jaunary", "february", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]
    ordinals = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", 
                "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", 
                "28th", "29th", "30th","31st"]
    return(f"Today is {week_now}, {month_list[month_now-1]} the {ordinals[day_now-1]}.")  

def weather_report():
    city = "Bangalore"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=93fd599f618326e21ea45bbbf973c216&units=metric"
    js = requests.get(weather_url).json()
    if js["cod"] != "404":
        weather = js["main"]
        current_temp = weather["temp"]
        max_temp = weather["temp_max"]
        min_temp = weather["temp_min"]
        humidity = weather["humidity"]
        weather_description = js["weather"][0]["description"]
        report = f"The Current weather in {city} is {weather_description} with current temperature {current_temp} degree celcius and humidity is {humidity}. The maximum temperature can go upto {max_temp} degree celcius and minimum temperature can go upto {min_temp} degree celcius."
    else:
        report= f"Sorry, but I couldn't find the weather report for {city}."
    return(report)

report = weather_report()
speak(report)