import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Sample dummy data (replace with your actual dataset)
data = pd.DataFrame({
    'PM2.5': [35, 55, 150, 85, 120],
    'PM10': [40, 70, 180, 100, 160],
    'NO': [10, 20, 30, 15, 25],
    'NO2': [15, 25, 40, 20, 30],
    'CO': [0.5, 1.2, 2.0, 1.0, 1.5],
    'SO2': [5, 10, 15, 8, 12],
    'O3': [20, 35, 50, 25, 40],
    'AQI': [50, 100, 200, 130, 180]
})

X = data.drop('AQI', axis=1)
y = data['AQI']

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save model
joblib.dump(model, "aqi_rf_best.pkl")
print("Model saved as aqi_rf_best.pkl")

