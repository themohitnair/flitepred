import pandas as pd

input_file = "dataset/processed/jfk_top5_dests_top3_carriers.csv"
output_file = "dataset/processed/jfk_final_2024.csv"

df = pd.read_csv(input_file)

df.rename(
    columns={
        "MONTH": "month",
        "DAY_OF_MONTH": "day_of_month",
        "DAY_OF_WEEK": "day_of_week",
        "OP_UNIQUE_CARRIER": "airline_carrier",
        "DEST_AIRPORT_ID": "destination_airport_id",
        "DEP_TIME": "departure_time",
        "DEP_DELAY": "departure_delay",
        "AIR_TIME": "air_time",
        "DISTANCE": "distance",
        "DEP_HOUR": "departure_hour",
        "DEP_MINUTE": "departure_minute",
        "temperature_2m": "temperature_celsius",
        "precipitation": "precipitation_mm",
        "cloudcover": "cloud_cover_percentage",
        "windspeed_10m": "wind_speed_mps",
        "weathercode": "weather_code",
    },
    inplace=True,
)

df.to_csv(output_file, index=False)

print("Columns have been renamed to lowercase.")
print(df.columns)
print(f"Renamed data saved to: {output_file}")
