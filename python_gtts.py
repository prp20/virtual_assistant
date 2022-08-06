from __future__ import print_function
import speech_recognition as sr
from time import ctime
import utils
from assisstant_tasks import tasks_asst
from weather_service import weather_report
from smart_chat import smart_chat


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
        utils.respond("I'm sorry. I could'n get you. Can you please repeat?")
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        utils.respond("I'm sorry. I could'n get you. Can you please repeat?")
        print("Request Failed; {0}".format(e))
    except Exception as e:
        utils.respond("I'm sorry. I could'n get you. Can you please repeat?")
        print(f"Exception: {e}")
    
    return data.lower()

def digital_assistant(data):
    global retry
    print("Calling smart chat !!!")
    intent, response = smart_chat(data)
    print("In digital assistant \n")
    if "how are you" in data:
        listening = True
        utils.respond("Thank you. I feel wonderful and well. Hope you feel the same.")

    elif "time" == intent:
        listening = True
        response = response + ctime()
        utils.respond(response)
        
    elif "weather" == intent:
        report = weather_report()
        response = response + report
        listening = True
        utils.respond(response)

    elif "event" in data or "plan" in data:
        import calender_services
        SERVICE = utils.authenticate_google()
        date = utils.get_date(data)
        if date:
            calender_services.calender_services(date, SERVICE)
        else:
            utils.respond("Please Try Again")
        listening = True
    elif "tasks" in data or "task" in data:
        tasks_asst(data)
        listening = True
    elif "thank you" in data:
        utils.respond("Thank you. Wake me if you need any help. Have a good day. Byeeeee")
        listening = False
        print('Listening stopped')
        return listening
    else:
        utils.respond("I'm sorry. I could'n get you. Can you please repeat?")
        listening = True
        retry=retry+1

    return listening

# time.sleep(2)
utils.respond("Hi Prasad, how can I help you? Please tell me")
listening = True
while listening == True and retry < 3:
    data = listen()
    listening = digital_assistant(data)
if listening:
    digital_assistant("thank you")
