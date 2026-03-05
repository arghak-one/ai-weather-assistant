import speech_recognition as sr
import pyttsx3
from agent import ask_weather_ai

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak your weather question...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print("You said:", query)
        return query
    except:
        return None


while True:

    query = listen()

    if not query:
        speak("Sorry I did not understand")
        continue

    if "exit" in query.lower():
        speak("Goodbye")
        break

    weather = ask_weather_ai(query)

    response = f"The temperature is {weather['temperature']} degree celsius with {weather['description']}"

    print(response)
    speak(response)