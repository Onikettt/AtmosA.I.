import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import webbrowser
import random
import wikipedia
from requests import get
import pywhatkit as kit
import sys
import openai

# Replacing 'YOUR_OPENAI_API_KEY' with my actual API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as audio:
        speak('Listening...')
        r.pause_threshold = 1
        try:
            voice = r.listen(audio, timeout=10, phrase_time_limit=5)
            print("Thinking...")
            query = r.recognize_google(voice, language='en-in')
            print("Transcription:" + query)
            return query
        except sr.UnknownValueError:
            print("I couldn't understand what you said.")
            return "none"
        except sr.RequestError:
            print("There was an issue with the speech recognition service.")
            return "none"

def chat_with_gpt3(query):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=query,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error in GPT-3 API:", e)
        return "I'm sorry, there was an issue with my response."


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good Evening")

    speak("Im Atmos AI, Is there anything I can help you with?")


if __name__ == "__main__":
    speak("Hello Sir!")
    wish()
    while True:

        query = takecommand().lower()

        # logic building for tasks
        if "open notepad" in query:
            npath = "C://Windows//notepad.exe"
            os.startfile(npath)
        elif "launch chrome" in query:
            webbrowser.open('https://www.google.com/')
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "open Discord" in query:
            ipath = "C:/Users/anida/AppData/Local/Discord/app-1.0.9015/Discord.exe"
            os.startfile(ipath)
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "C://Users/anida/PycharmProjects/Atmos_AI/music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile((os.path.join(music_dir, rd)))

        elif "ip address" in query:
            ip = get('http://api.ipify.org').text
            speak(f"your IP Address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            print(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open google" in query:
            speak("sir,what should I search on Google")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send message" in query:
            kit.sendwhatmsg("+917439897125", "This is a testing message from Atmos AI.", 2, 25)

        elif "play song on youtube" in query:
            kit.playonyt("A Thousand Years")


        elif "no" in query or "no thanks" in query:
            speak("Thanks for using me Sir, have a good day.")
            sys.exit()

        chat_response = chat_with_gpt3(query)
        speak(chat_response)
        speak("Sir do you have any other work?")
