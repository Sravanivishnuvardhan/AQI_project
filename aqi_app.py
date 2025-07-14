import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Load model
model = joblib.load("aqi_rf_best.pkl")

# Custom AQI Category function
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good ✅", "green"
    elif aqi <= 100:
        return "Moderate ☁️", "yellow"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups ⚠️", "orange"
    elif aqi <= 200:
        return "Unhealthy 😷", "red"
    else:
        return "Very Unhealthy 🚨", "maroon"

# Title
st.title("🌫️ Air Quality Index (AQI) Prediction Dashboard")

st.markdown("Enter the pollutant concentrations below or use a sample city data button:")

# Preset Buttons
preset_city = st.radio("Choose Sample Data:", ["Custom Input", "Delhi", "Mumbai", "Hyderabad"], horizontal=True)

if preset_city == "Delhi":
    pm25, pm10, no, no2, co, so2, o3 = 180, 250, 60, 90, 2.5, 20, 30
elif preset_city == "Mumbai":
    pm25, pm10, no, no2, co, so2, o3 = 75, 110, 25, 40, 1.2, 15, 45
elif preset_city == "Hyderabad":
    pm25, pm10, no, no2, co, so2, o3 = 65, 90, 18, 35, 1.0, 12, 40
else:
    col1, col2 = st.columns(2)
    with col1:
        pm25 = st.slider("PM2.5 (µg/m³)", 0.0, 500.0, 50.0)
        pm10 = st.slider("PM10 (µg/m³)", 0.0, 500.0, 80.0)
        no = st.slider("NO (µg/m³)", 0.0, 100.0, 20.0)
    with col2:
        no2 = st.slider("NO2 (µg/m³)", 0.0, 200.0, 30.0)
        co = st.slider("CO (mg/m³)", 0.0, 10.0, 1.0)
        so2 = st.slider("SO2 (µg/m³)", 0.0, 100.0, 10.0)
        o3 = st.slider("O3 (µg/m³)", 0.0, 150.0, 25.0)

# Predict button
if st.button("🔍 Predict AQI"):
    input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
    prediction = model.predict(input_data)[0]
    category, color = get_aqi_category(prediction)

    # Result
    st.markdown(f"### 📈 Predicted AQI: `{int(prediction)}`")
    st.markdown(f"<span style='color:{color}; font-size:20px;'>Category: {category}</span>", unsafe_allow_html=True)

    # Chart
    pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'CO', 'SO2', 'O3']
    values = [pm25, pm10, no, no2, co, so2, o3]

    fig, ax = plt.subplots()
    ax.bar(pollutants, values, color='skyblue')
    ax.set_ylabel('Concentration')
    ax.set_title('Pollutant Levels')
    st.pyplot(fig)
