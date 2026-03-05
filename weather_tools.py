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


def get_forecast(city):

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    r = requests.get(url).json()

    if r.get("cod") != "200":
        return {"error": "Forecast not found"}

    data = []

    for item in r["list"][:8]:

        data.append({
            "time": item["dt_txt"],
            "temperature": item["main"]["temp"]
        })

    return data


def get_air_quality(city):

    geo = requests.get(
        f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    ).json()

    if not geo:
        return {"error": "City not found"}

    lat = geo[0]["lat"]
    lon = geo[0]["lon"]

    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    r = requests.get(url).json()

    return {
        "aqi": r["list"][0]["main"]["aqi"]
    }