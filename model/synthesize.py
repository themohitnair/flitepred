import joblib
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

os.makedirs("model", exist_ok=True)

df = pd.read_csv("dataset/processed/jfk_encoded_2024.csv")

X = df.drop(columns=["departure_delay"])
y = df["departure_delay"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestRegressor()
model.fit(X_scaled, y)

y_pred = model.predict(X_scaled)

joblib.dump(model, "model/model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
