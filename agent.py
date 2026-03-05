from weather_tools import (
    get_current_weather,
    get_forecast,
    get_air_quality
)


def ask_weather_ai(query):

    query = query.lower()

    # CURRENT WEATHER
    if "weather in" in query:

        city = query.replace("weather in", "").strip()

        return get_current_weather(city)


    # FORECAST
    elif "forecast in" in query:

        city = query.replace("forecast in", "").strip()

        return get_forecast(city)


    # AIR QUALITY
    elif "air quality in" in query:

        city = query.replace("air quality in", "").strip()

        return get_air_quality(city)


    return {"error": "City not found"}