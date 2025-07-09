import streamlit as st
import subprocess

st.write("Installed packages:")
st.code(subprocess.getoutput("pip list"))

import streamlit as st
import joblib
import numpy as np

# Load the saved model
model = joblib.load("aqi_rf_best.pkl")

st.title("Air Quality Index (AQI) Predictor")

st.markdown("Enter the pollutant levels below to predict the AQI and get a health suggestion.")

# User inputs
pm25 = st.number_input("PM2.5", min_value=0.0)
pm10 = st.number_input("PM10", min_value=0.0)
no = st.number_input("NO", min_value=0.0)
no2 = st.number_input("NO2", min_value=0.0)
co = st.number_input("CO", min_value=0.0)
so2 = st.number_input("SO2", min_value=0.0)
o3 = st.number_input("O3", min_value=0.0)

def get_aqi_suggestion(aqi):
    if aqi <= 50:
        return "Air quality is Good 😊. No precautions needed."
    elif aqi <= 100:
        return "Air quality is Moderate 🙂. Sensitive individuals may feel minor effects."
    elif aqi <= 150:
        return "Air quality is Unhealthy for sensitive groups 😷. People with respiratory issues should avoid outdoor activity."
    elif aqi <= 200:
        return "Air quality is Unhealthy 😷. Wearing a mask and avoiding heavy outdoor activity is recommended."
    elif aqi <= 300:
        return "Air quality is Very Unhealthy 😫. Stay indoors and use air purifiers if possible."
    else:
        return "Hazardous! 🛑 Serious health effects. Stay indoors and avoid exposure."

# Predict button
if st.button("Predict AQI"):
    input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted AQI: {prediction:.2f}")
    suggestion = get_aqi_suggestion(prediction)
    st.info(suggestion)

