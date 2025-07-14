import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
import io

# Load the model
model = joblib.load("aqi_rf_best.pkl")

# Configure the page
st.set_page_config(page_title="AQI Predictor", layout="centered", page_icon="🌫️")

# Function to determine AQI category and associated color
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good ✅", "#00e400", "Enjoy the day!"
    elif aqi <= 100:
        return "Moderate ☁️", "#ffff00", "Okay for most."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups ⚠️", "#ff7e00", "Consider wearing a mask."
    elif aqi <= 200:
        return "Unhealthy 😷", "#ff0000", "Wear a mask and limit outdoor time."
    else:
        return "Very Unhealthy 🚨", "#8f3f97", "Stay indoors!"

# Sidebar navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📥 Predict AQI", "📊 Visualize", "📄 Download Report"])

# Initialize session state
if "prediction" not in st.session_state:
    st.session_state.prediction = None
    st.session_state.input_values = {}

# ---------------------- HOME PAGE ----------------------
if page == "🏠 Home":
    st.title("🌫️ AQI Prediction Web App")
    st.markdown("""
    Welcome to the **Air Quality Index Prediction App**.
    
    This tool allows you to:
    - Enter pollution values to predict AQI
    - Visualize input data
    - Download a personalized AQI report
    """)
    st.image("https://images.unsplash.com/photo-1603145733144-62a449453dba", width=700)

# ---------------------- PREDICT PAGE ----------------------
elif page == "📥 Predict AQI":
    st.title("📥 Enter Pollution Data to Predict AQI")
    st.markdown("Use the fields below to input pollution levels:")

    col1, col2, col3 = st.columns(3)
    with col1:
        pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 500.0, 50.0)
        no = st.number_input("NO (µg/m³)", 0.0, 200.0, 20.0)
        co = st.number_input("CO (mg/m³)", 0.0, 10.0, 1.0)
    with col2:
        pm10 = st.number_input("PM10 (µg/m³)", 0.0, 500.0, 80.0)
        no2 = st.number_input("NO2 (µg/m³)", 0.0, 200.0, 30.0)
        so2 = st.number_input("SO2 (µg/m³)", 0.0, 200.0, 10.0)
    with col3:
        o3 = st.number_input("O3 (µg/m³)", 0.0, 200.0, 25.0)

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

        # Custom styled result box (no yellow default box)
        st.markdown(f"""
        <div style='
            padding: 15px;
            background-color: {color};
            border-radius: 10px;
            color: black;
            font-size: 18px;
        '>
            <b>Predicted AQI:</b> {int(prediction)}<br>
            <b>Category:</b> {category}<br>
            <b>Advice:</b> {advice}
        </div>
        """, unsafe_allow_html=True)

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

# ---------------------- DOWNLOAD REPORT PAGE ----------------------
elif page == "📄 Download Report":
    st.title("📄 Download AQI Report")
    if st.session_state.prediction:
        data = st.session_state.input_values
        report = f"""
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
        """
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="AQI_Report.txt",
            mime="text/plain"
        )
        st.code(report)
    else:
        st.info("⚠️ No AQI prediction found. Please go to the Predict page first.")

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("🔬 Built with ❤️ by Sravani | Powered by Streamlit & Machine Learning")
