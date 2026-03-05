from groq import Groq
import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env file (for running on your PC)
load_dotenv()

# Try Streamlit secrets first, fallback to environment variable
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)


def ai_weather_chat(question, weather_data):
    prompt = f"""
You are a smart weather assistant.

User question:
{question}

Weather data:
{weather_data}

Explain the weather clearly and naturally for the user.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=300
    )

    return response.choices[0].message.content