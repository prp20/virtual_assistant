import requests
from decouple import config

API_KEY = config("WEATHER_API_KEY")
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