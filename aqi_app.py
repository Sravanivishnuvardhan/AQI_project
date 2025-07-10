import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ------------------- Custom Dashboard Styling -------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }
    .stNumberInput > div > input {
        background-color: #1e1e1e;
        color: white;
    }
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        margin-top: 10px;
    }
    .stDownloadButton > button {
        background-color: #4caf50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Sidebar Info -------------------
st.sidebar.title("📘 About the AQI Dashboard")
st.sidebar.markdown("""
This dashboard predicts **Air Quality Index (AQI)** using pollutant concentrations.

### Instructions
- Modify the default pollutant values or use your own
- View the pie chart distribution
- Get AQI score, category, and health advice
- Download a report for offline use
""")

# ------------------- Load Model -------------------
model = joblib.load("aqi_rf_best.pkl")

# ------------------- Title -------------------
st.title("🌫️ Air Quality Dashboard")

st.markdown("### 🧪 Enter Pollutant Levels (Defaults are for Example City AQI)")
col1, col2, col3 = st.columns(3)

with col1:
    pm25 = st.number_input("PM2.5 (μg/m³)", min_value=0.0, value=85.0, step=1.0)
    no = st.number_input("NO (ppb)", min_value=0.0, value=20.0, step=1.0)
    co = st.number_input("CO (mg/m³)", min_value=0.0, value=1.2, step=0.1)
with col2:
    pm10 = st.number_input("PM10 (μg/m³)", min_value=0.0, value=120.0, step=1.0)
    no2 = st.number_input("NO2 (ppb)", min_value=0.0, value=40.0, step=1.0)
    o3 = st.number_input("O3 (ppb)", min_value=0.0, value=30.0, step=1.0)
with col3:
    so2 = st.number_input("SO2 (ppb)", min_value=0.0, value=15.0, step=1.0)

# ------------------- Pie Chart -------------------
st.markdown("### 📊 Pollutant Contribution")

labels = ['PM2.5', 'PM10', 'NO', 'NO2', 'CO', 'SO2', 'O3']
values = [pm25, pm10, no, no2, co, so2, o3]

if sum(values) > 0:
    fig, ax = plt.subplots(facecolor='#121212')
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color': 'white'})
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.warning("⚠️ Please enter pollutant values to view the chart.")

# ------------------- AQI Category Helper -------------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "✅ Air quality is satisfactory. No precautions needed."
    elif aqi <= 100:
        return "Moderate", "🟡 Acceptable, but sensitive groups should reduce outdoor activity."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "🟠 People with conditions should limit prolonged exertion."
    elif aqi <= 200:
        return "Unhealthy", "🔴 Everyone should reduce outdoor exposure."
    elif aqi <= 300:
        return "Very Unhealthy", "🟣 Health alert: wear a mask and stay indoors."
    else:
        return "Hazardous", "⚫ Emergency: Remain indoors, avoid all outdoor activity."

# ------------------- Predict Button -------------------
if st.button("🔮 Predict AQI"):
    input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
    prediction = model.predict(input_data)
    aqi_value = int(prediction[0])
    category, advice = get_aqi_category(aqi_value)

    st.markdown("### ✅ Prediction Result")
    st.success(f"**Predicted AQI**: `{aqi_value}`  — **{category}**")
    st.info(f"**Health Advice**: {advice}")

    # ------------------- Download Report -------------------
    result = pd.DataFrame({
        "AQI": [aqi_value],
        "Category": [category],
        "Advice": [advice]
    })

    st.download_button("📥 Download Report as CSV", result.to_csv(index=False), "aqi_report.csv", "text/csv")
