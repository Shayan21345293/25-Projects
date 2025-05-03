import streamlit as st
import requests

st.set_page_config(page_title="Weather App", page_icon="☁️")

st.title("☁️ Simple Weather App")
st.subheader("Get live weather data of any city 🌍")
api_key='9a641e963d4d88b86f9f6e1e5e83d3c0'

# City input
city = st.text_input("🏙️ Enter city name")

if st.button("Get Weather") and api_key and city:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            st.error(f"Error: {data['message']}")
        else:
            st.success(f"Weather in {data['name']}, {data['sys']['country']}")
            st.metric("🌡️ Temperature", f"{data['main']['temp']} °C")
            st.metric("💧 Humidity", f"{data['main']['humidity']}%")
            st.metric("🌬️ Wind Speed", f"{data['wind']['speed']} m/s")
            st.write(f"☁️ Description: `{data['weather'][0]['description']}`")
    except Exception as e:
        st.error("Failed to fetch data. Check your internet or API key.")
