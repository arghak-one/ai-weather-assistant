import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    r = requests.get(url).json()

    if r.get("cod") != 200:
        return {"error": "City not found"}

    return {
        "temperature": r["main"]["temp"],
        "humidity": r["main"]["humidity"],
        "wind_speed": r["wind"]["speed"],
        "description": r["weather"][0]["description"]
    }