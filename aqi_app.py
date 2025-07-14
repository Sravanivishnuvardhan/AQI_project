import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
import io

# Load model
model = joblib.load("aqi_rf_best.pkl")

# App config
st.set_page_config(page_title="AQI Predictor", layout="centered", page_icon="🌫️")

# Custom function to get AQI Category
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good ✅", "green", "Enjoy the day!"
    elif aqi <= 100:
        return "Moderate ☁️", "yellow", "Okay for most."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups ⚠️", "orange", "Consider wearing a mask."
    elif aqi <= 200:
        return "Unhealthy 😷", "red", "Wear a mask and limit outdoor time."
    else:
        return "Very Unhealthy 🚨", "maroon", "Stay indoors!"

# Sidebar navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📥 Predict AQI", "📊 Visualize", "📄 Download Report"])

# Global state variables
if "prediction" not in st.session_state:
    st.session_state.prediction = None
    st.session_state.input_values = {}

# ---------------------- HOME PAGE ----------------------
if page == "🏠 Home":
    st.title("🌫️ AQI Prediction Web App")
    st.markdown("""
    Welcome to the **Air Quality Index Prediction App**.
    
    - Enter pollutant values to predict AQI.
    - Get a color-coded air quality category.
    - Download the result as a report.
    - Visualize the pollutant input levels.
    """)
    st.image("https://images.unsplash.com/photo-1603145733144-62a449453dba", width=700)

# ---------------------- PREDICT PAGE ----------------------
elif page == "📥 Predict AQI":
    st.title("📥 Enter Pollution Data to Predict AQI")
    st.markdown("Adjust the pollutant levels below:")

    # Layout with columns
    col1, col2, col3 = st.columns(3)
    with col1:
        pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, value=50.0)
        no = st.number_input("NO (µg/m³)", min_value=0.0, value=20.0)
        co = st.number_input("CO (mg/m³)", min_value=0.0, value=1.0)
    with col2:
        pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, value=80.0)
        no2 = st.number_input("NO2 (µg/m³)", min_value=0.0, value=30.0)
        so2 = st.number_input("SO2 (µg/m³)", min_value=0.0, value=10.0)
    with col3:
        o3 = st.number_input("O3 (µg/m³)", min_value=0.0, value=25.0)

    if st.button("🔍 Predict AQI"):
        input_data = np.array([[pm25, pm10, no, no2, co, so2, o3]])
        prediction = model.predict(input_data)[0]
        category, color, advice = get_aqi_category(prediction)

        st.session_state.prediction = int(prediction)
        st.session_state.input_values = {
            "PM2.5": pm25, "PM10": pm10, "NO": no, "NO2": no2,
            "CO": co, "SO2": so2, "O3": o3,
            "category": category, "color": color, "advice": advice
        }

        st.markdown(f"### 🧪 Predicted AQI: `{int(prediction)}`")
        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:8px;'>"
                    f"<h5 style='color:white;'>Category: {category}</h5>"
                    f"<p style='color:white;'>{advice}</p></div>", unsafe_allow_html=True)

# ---------------------- VISUALIZATION PAGE ----------------------
elif page == "📊 Visualize":
    st.title("📊 Pollutant Input Levels")
    if st.session_state.prediction:
        pollutants = list(st.session_state.input_values.keys())[:-3]
        values = [st.session_state.input_values[p] for p in pollutants]
        fig, ax = plt.subplots()
        ax.bar(pollutants, values, color='skyblue')
        ax.set_ylabel("Concentration")
        ax.set_title("Pollutant Levels")
        st.pyplot(fig)
    else:
        st.info("⚠️ Please predict AQI first to view visualizations.")

# ---------------------- DOWNLOAD PAGE ----------------------
elif page == "📄 Download Report":
    st.title("📄 Download AQI Report")
    if st.session_state.prediction:
        data = st.session_state.input_values
        report = f\"\"\"
Air Quality Prediction Report
-----------------------------
PM2.5: {data['PM2.5']} µg/m³
PM10: {data['PM10']} µg/m³
NO: {data['NO']} µg/m³
NO2: {data['NO2']} µg/m³
CO: {data['CO']} mg/m³
SO2: {data['SO2']} µg/m³
O3: {data['O3']} µg/m³

Predicted AQI: {st.session_state.prediction}
Category: {data['category']}
Advice: {data['advice']}
        \"\"\"
        buffer = io.StringIO()
        buffer.write(report)
        buffer.seek(0)
        st.download_button("📥 Download Report", buffer, "AQI_Report.txt", "text/plain")
        st.code(report)
    else:
        st.info("⚠️ No AQI prediction found. Please go to the Predict page first.")

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("🔬 Built with ❤️ by Sravani | Powered by Streamlit & ML")
