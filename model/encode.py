import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("dataset/processed/jfk_final_2024.csv")

kf = KFold(n_splits=5, shuffle=True, random_state=42)
target_col = "departure_delay"

for col in ["airline_carrier", "destination_airport_id"]:
    encoded = np.zeros(df.shape[0])
    for train_idx, valid_idx in kf.split(df):
        train_fold, valid_fold = df.iloc[train_idx], df.iloc[valid_idx]
        means = train_fold.groupby(col)[target_col].mean()
        encoded[valid_idx] = valid_fold[col].map(means)
    df[f"{col}_target_enc"] = encoded


def encode_cyclical(df, col, max_val):
    df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / max_val)
    df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / max_val)


encode_cyclical(df, "month", 12)
encode_cyclical(df, "day_of_week", 7)
encode_cyclical(df, "departure_hour", 24)
encode_cyclical(df, "departure_minute", 60)

weather_labels = {
    0: "clear_sky",
    1: "mainly_clear",
    2: "partly_cloudy",
    3: "overcast",
    45: "fog",
    48: "rime_fog",
    51: "light_drizzle",
    53: "moderate_drizzle",
    55: "dense_drizzle",
    56: "light_freezing_drizzle",
    57: "dense_freezing_drizzle",
    61: "slight_rain",
    63: "moderate_rain",
    65: "heavy_rain",
    66: "light_freezing_rain",
    67: "heavy_freezing_rain",
    71: "slight_snow",
    73: "moderate_snow",
    75: "heavy_snow",
    77: "snow_grains",
    80: "slight_rain_showers",
    81: "moderate_rain_showers",
    82: "violent_rain_showers",
    85: "slight_snow_showers",
    86: "heavy_snow_showers",
    95: "thunderstorm",
    96: "thunderstorm_light_hail",
    99: "thunderstorm_heavy_hail",
}

df["weather_desc"] = df["weather_code"].map(weather_labels)
df = pd.get_dummies(df, columns=["weather_desc"], prefix="weather")

num_cols = [
    "distance",
    "air_time",
    "temperature_celsius",
    "precipitation_mm",
    "cloud_cover_percentage",
    "wind_speed_mps",
]
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

drop_cols = [
    "airline_carrier",
    "destination_airport_id",
    "departure_time",
    "weather_code",
    "month",
    "day_of_week",
    "departure_hour",
    "departure_minute",
]
df.drop(columns=drop_cols, inplace=True)

df.to_csv("dataset/processed/jfk_encoded_2024.csv", index=False)
print("✅ Done! Clean, encoded data saved.")
