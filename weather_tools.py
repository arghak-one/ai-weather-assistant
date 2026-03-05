import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load local env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    API_KEY = st.secrets.get("OPENWEATHER_API_KEY")


# -------------------------
# CURRENT WEATHER
# -------------------------

def get_current_weather(city):

    if not API_KEY:
        return {"error": "API key not configured"}

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        r = requests.get(url, timeout=10)
        data = r.json()

        if r.status_code != 200:
            return {"error": data.get("message", "City not found")}

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# AIR QUALITY
# -------------------------

def get_air_quality(city):

    if not API_KEY:
        return {"error": "API key not configured"}

    try:
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"

        geo = requests.get(geo_url).json()

        if not geo:
            return {"error": "City not found"}

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

        r = requests.get(air_url).json()

        return {
            "aqi": r["list"][0]["main"]["aqi"]
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------
# 5 DAY FORECAST
# -------------------------

def get_forecast(city):

    if not API_KEY:
        return {"error": "API key not configured"}

    try:

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        r = requests.get(url).json()

        temps = []
        times = []

        for item in r["list"][:8]:
            temps.append(item["main"]["temp"])
            times.append(item["dt_txt"])

        return {
            "temps": temps,
            "times": times
        }

    except Exception as e:
        return {"error": str(e)}