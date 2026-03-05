from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_weather_chat(question, weather_data):

    prompt = f"""
You are a smart weather assistant.

User question:
{question}

Weather data:
{weather_data}

Answer the question naturally.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content