import pandas as pd

weather_df = pd.read_csv("dataset/raw/jfk_weather_2014_24.csv")

weather_df["valid"] = pd.to_datetime(weather_df["valid"], errors="coerce")

weather_df = weather_df[~weather_df["valid"].dt.year.isin([2020, 2021])]

weather_df = weather_df.drop(columns=["station"])

weather_df["YEAR"] = weather_df["valid"].dt.year
weather_df["MONTH"] = weather_df["valid"].dt.month
weather_df["DAY_OF_MONTH"] = weather_df["valid"].dt.day


weather_df["TIME"] = weather_df["valid"].dt.hour * 100 + weather_df["valid"].dt.minute


weather_df = weather_df.drop(columns=["valid"])

cols = ["YEAR", "MONTH", "DAY_OF_MONTH", "TIME"] + [
    col
    for col in weather_df.columns
    if col not in ["YEAR", "MONTH", "DAY_OF_MONTH", "TIME"]
]
weather_df = weather_df[cols]

weather_df.to_csv("dataset/processed_data/weather_cleaned.csv", index=False)

print("Weather dataset cleaned and saved as 'weather_cleaned.csv'")
