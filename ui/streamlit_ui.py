import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import re
import io
import speech_recognition as sr

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent import ask_weather_ai
from ai_chat import ai_weather_chat


# -----------------------------
# CITY EXTRACTOR
# -----------------------------

def extract_city(question):

    question = question.lower()

    match = re.search(r"in ([a-zA-Z ]+)", question)

    if match:
        return match.group(1).strip()

    return None


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
page_title="AI Weather Dashboard",
page_icon="🌤",
layout="wide"
)




st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>

/* ---------- GLOBAL ---------- */
html, body, [class*="css"]{
font-family:'Poppins',sans-serif;
}

/* ---------- BACKGROUND ---------- */
.stApp{
background: linear-gradient(120deg,#0f2027,#203a43,#2c5364,#1e3c72);
background-size:400% 400%;
animation:gradientMove 18s ease infinite;
color:white;
}

@keyframes gradientMove{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}


/* ---------- TITLE ---------- */
h1{
font-size:65px;
font-weight:700;
background:linear-gradient(90deg,#00f2fe,#4facfe,#43e97b);
-webkit-background-clip:text;
color:transparent;
animation:glow 3s ease-in-out infinite alternate;
}

@keyframes glow{
from{filter:drop-shadow(0 0 5px #00f2fe);}
to{filter:drop-shadow(0 0 25px #43e97b);}
}


/* ---------- BUTTON ---------- */
.stButton button{
background:linear-gradient(90deg,#00c6ff,#0072ff,#00f2fe);
color:white;
border:none;
border-radius:12px;
padding:12px 28px;
font-weight:600;
font-size:16px;
box-shadow:0 10px 25px rgba(0,0,0,0.4);
transition:all .3s ease;
}

.stButton button:hover{
transform:scale(1.1);
background:linear-gradient(90deg,#43e97b,#38f9d7);
box-shadow:0 20px 50px rgba(0,0,0,0.7);
}


/* ---------- INPUT ---------- */
.stTextInput input{
background:rgba(255,255,255,0.12);
border-radius:12px;
border:1px solid rgba(255,255,255,0.25);
color:white;
padding:12px;
}


/* ---------- METRIC CARDS ---------- */
[data-testid="metric-container"]{
background:rgba(255,255,255,0.08);
border-radius:18px;
padding:20px;
backdrop-filter:blur(15px);
border:1px solid rgba(255,255,255,0.15);
box-shadow:0 10px 30px rgba(0,0,0,0.5);
transition:all .3s ease;
}

[data-testid="metric-container"]:hover{
transform:translateY(-10px) scale(1.05);
box-shadow:0 30px 60px rgba(0,0,0,0.8);
}


/* ---------- CHART BOX ---------- */
.element-container:has(.js-plotly-plot){
background:rgba(255,255,255,0.05);
border-radius:20px;
padding:20px;
backdrop-filter:blur(10px);
border:1px solid rgba(255,255,255,0.1);
}


/* ---------- FLOATING CLOUD ---------- */
.cloud{
position:absolute;
top:100px;
left:-200px;
width:200px;
height:60px;
background:white;
border-radius:60px;
opacity:0.12;
animation:cloudmove 50s linear infinite;
}

@keyframes cloudmove{
0%{left:-200px;}
100%{left:120%;}
}


/* ---------- SUN ---------- */
.sun{
position:absolute;
top:70px;
right:70px;
width:120px;
height:120px;
background:radial-gradient(circle,#ffd700,#ff9800);
border-radius:50%;
box-shadow:0 0 80px rgba(255,200,0,0.7);
animation:spin 20s linear infinite;
}

@keyframes spin{
0%{transform:rotate(0deg);}
100%{transform:rotate(360deg);}
}

</style>

<div class="sun"></div>
<div class="cloud"></div>

""", unsafe_allow_html=True)
# -----------------------------
# TITLE
# -----------------------------

st.title("AI Weather Intelligence Dashboard")
st.write("Get real-time weather, forecast, and air quality data.")


# -----------------------------
# WEATHER SEARCH
# -----------------------------

city = st.text_input("Enter City Name")

if st.button("Get Weather"):

    # Check if city entered
    if city.strip() == "":
        st.warning("Please enter a city name")
        st.stop()

    try:

        weather = ask_weather_ai(f"weather in {city}")

        # Debug (remove later if you want)
        st.write(weather)

        # Validate weather data
        if isinstance(weather, dict) and "temperature" in weather:

            st.subheader(f"Current Weather in {city.title()}")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("🌡 Temperature", f"{weather['temperature']} °C")
            col2.metric("💧 Humidity", f"{weather['humidity']} %")
            col3.metric("🌬 Wind Speed", f"{weather['wind_speed']} m/s")
            col4.metric("☀ Condition", weather["description"].title())

            # -----------------------------
            # FORECAST
            # -----------------------------

            forecast = ask_weather_ai(f"forecast in {city}")

            if isinstance(forecast, list):

                df = pd.DataFrame(forecast)

                st.subheader("📊 Temperature Forecast")

                fig = px.line(
                    df,
                    x="time",
                    y="temperature",
                    markers=True,
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)

            # -----------------------------
            # AIR QUALITY
            # -----------------------------

            aqi = ask_weather_ai(f"air quality in {city}")

            if isinstance(aqi, dict) and "aqi" in aqi:

                st.subheader("🌫 Air Quality")
                st.metric("AQI", aqi["aqi"])

        else:
            st.error("Weather data could not be fetched.")

    except Exception as e:
        st.error("Something went wrong while fetching weather data.")
        st.write(e)
# -----------------------------
# WEATHER MAP
# -----------------------------

st.subheader("🌍 Global Weather Map")

st.components.v1.iframe(
"https://embed.windy.com/embed2.html",
height=500
)


# -----------------------------
# AI WEATHER CHATBOT (TEXT)
# -----------------------------

st.subheader("🤖 AI Weather Assistant")

question = st.text_input("Ask anything about weather")

if st.button("Ask AI"):

    if question.strip()=="":
        st.warning("Please type a question")
        st.stop()

    with st.spinner("AI thinking..."):

        try:

            city = extract_city(question)

            if city is None:
                st.error("Please mention a city. Example: 'weather in kolkata'")
                st.stop()

            weather_data = ask_weather_ai(f"weather in {city}")

            answer = ai_weather_chat(question, weather_data)

            st.success(answer)

        except Exception as e:

            st.error("AI could not process the request")
            st.write(e)



# -----------------------------
# VOICE WEATHER ASSISTANT
# -----------------------------

st.subheader("🎤 Speak your question")

audio_file = st.audio_input("Record your question")

if audio_file is not None:

    recognizer = sr.Recognizer()

    audio_bytes = audio_file.read()

    audio_stream = io.BytesIO(audio_bytes)

    with sr.AudioFile(audio_stream) as source:

        audio_data = recognizer.record(source)

    try:

        question = recognizer.recognize_google(audio_data)

        st.success(f"You said: {question}")

        city = extract_city(question)

        if city is None:

            st.error("Please mention a city in your question")

        else:

            weather_data = ask_weather_ai(f"weather in {city}")

            answer = ai_weather_chat(question, weather_data)

            st.success(answer)

    except Exception:

        st.error("Could not understand audio")