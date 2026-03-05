from weather_tools import get_current_weather

def ask_weather_ai(query):

    query = query.lower()

    if "weather in" in query:

        city = query.replace("weather in", "").strip()

        return get_current_weather(city)

    return {"error": "City not found"}