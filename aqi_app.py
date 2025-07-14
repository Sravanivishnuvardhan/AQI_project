import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("aqi_rf_best.pkl")

# Title
st.title("Air Quality Index (AQI) Prediction App")

# Input fields
pm25 = st.number_input("PM2.5", min_value=0.0, value=50.0)
pm10 = st.number_input("PM10", min_value=0.0, value=80.0)
no = st.number_input("NO", min_value=0.0, value=20.0)
no2 = st.number_input("NO2", min_value=0.0, value=30.0)
co = st.number_input("CO", min_value=0.0, value=1.0)
so2 = st.number_input("SO2", min_value=0.0, value=10.0)
o3 = st.number_input("O3", min_value=0.0, value=25.0)

# Predict button
if st.button("Predict AQI"):
    input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
    prediction = model.predict(input_data)[0]
    
    # Display result
    st.success(f"Predicted AQI: {int(prediction)}")

    # Suggest air quality status
    if prediction <= 50:
        st.info("Air Quality: Good ✅ - Enjoy the day!")
    elif prediction <= 100:
        st.info("Air Quality: Moderate ☁️ - Okay for most.")
    elif prediction <= 150:
        st.warning("Air Quality: Unhealthy for Sensitive Groups ⚠️ - Consider wearing a mask.")
    elif prediction <= 200:
        st.error("Air Quality: Unhealthy 😷 - Wear a mask and limit outdoor time.")
    else:
        st.error("Air Quality: Very Unhealthy 🚨 - Stay indoors!")

