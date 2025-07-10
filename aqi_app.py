import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ------------------- Custom Styling -------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- Sidebar Info -------------------
st.sidebar.title("📘 About the App")
st.sidebar.markdown("""
This app predicts **Air Quality Index (AQI)** using a trained machine learning model.

### Inputs
- PM2.5, PM10 (particulate matter)
- Gases: NO, NO2, CO, SO2, O3

### Output
- AQI value
- Air quality category
- Health advice
- Pie chart of pollutant contribution
- Downloadable report
""")

# ------------------- Load Model -------------------
model = joblib.load("aqi_rf_best.pkl")

# ------------------- Page Title -------------------
st.title("🌫️ Air Quality Index (AQI) Predictor")

# ------------------- Input Fields -------------------
st.subheader("📥 Enter Pollutant Values")

pm25 = st.number_input("PM2.5 (μg/m³)", min_value=0.0, help="Fine particulate matter")
pm10 = st.number_input("PM10 (μg/m³)", min_value=0.0, help="Coarse dust particles")
no = st.number_input("NO (ppb)", min_value=0.0)
no2 = st.number_input("NO2 (ppb)", min_value=0.0)
co = st.number_input("CO (mg/m³)", min_value=0.0)
so2 = st.number_input("SO2 (ppb)", min_value=0.0)
o3 = st.number_input("O3 (ppb)", min_value=0.0)

# ------------------- Pie Chart -------------------
st.subheader("📊 Pollutant Distribution")

labels = ['PM2.5', 'PM10', 'NO', 'NO2', 'CO', 'SO2', 'O3']
values = [pm25, pm10, no, no2, co, so2, o3]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# ------------------- AQI Category Logic -------------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "Air quality is satisfactory. No precautions needed."
    elif aqi <= 100:
        return "Moderate", "Acceptable air quality. Sensitive individuals should avoid outdoor exertion."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Limit outdoor activities if you have respiratory issues."
    elif aqi <= 200:
        return "Unhealthy", "Wear a mask and avoid prolonged outdoor activity."
    elif aqi <= 300:
        return "Very Unhealthy", "Everyone should avoid outdoor activity. Wear a high-quality mask."
    else:
        return "Hazardous", "Stay indoors. Use air purifiers. Seek medical help if needed."

# ------------------- Prediction -------------------
if st.button("🔮 Predict AQI"):
    input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
    prediction = model.predict(input_data)
    aqi_value = int(prediction[0])

    category, advice = get_aqi_category(aqi_value)

    st.success(f"✅ Predicted AQI: {aqi_value} ({category})")
    st.info(f"🩺 Health Advice: {advice}")

    # ------------------- Download Report -------------------
    result = pd.DataFrame({
        "AQI": [aqi_value],
        "Category": [category],
        "Advice": [advice]
    })

    st.download_button("📥 Download Report as CSV", result.to_csv(index=False), "aqi_report.csv", "text/csv")


