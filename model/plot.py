import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")
df = pd.read_csv("dataset/processed/jfk_final_2024.csv")
os.makedirs("plots", exist_ok=True)

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

if "weather_desc" not in df.columns:
    print("Error: 'weather_desc' column not found. Check if the mapping is correct.")
else:
    plt.figure(figsize=(10, 5))
    sns.histplot(df["departure_delay"], bins=50, kde=True)
    plt.title("Departure Delay Distribution")
    plt.xlabel("Delay (minutes)")
    plt.ylabel("Frequency")
    plt.savefig("plots/departure_delay_distribution.png", dpi=500)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=df,
        x="airline_carrier",
        y="departure_delay",
        estimator=lambda x: sum(x) / len(x),
        errorbar=None,
    )
    plt.title("Average Departure Delay by Airline")
    plt.ylabel("Average Delay (min)")
    plt.savefig("plots/average_delay_by_airline.png", dpi=500)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.countplot(
        data=df,
        x="destination_airport_id",
        order=df["destination_airport_id"].value_counts().index,
    )
    plt.title("Flight Count by Destination Airport")
    plt.ylabel("Number of Flights")
    plt.xlabel("Destination Airport ID")
    plt.savefig("plots/flight_count_by_destination.png", dpi=500)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="temperature_celsius",
        y="departure_delay",
        hue="weather_code",
        alpha=0.6,
    )
    plt.title("Departure Delay vs. Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Delay (min)")
    plt.savefig("plots/delay_vs_temperature.png", dpi=500)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.boxenplot(data=df, x="weather_code", y="departure_delay")
    plt.title("Delays by Weather Code")
    plt.xlabel("Weather Code")
    plt.ylabel("Departure Delay (min)")
    plt.savefig("plots/delays_by_weather_code.png", dpi=500)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.boxenplot(data=df, x="departure_hour", y="departure_delay")
    plt.title("Departure Delay by Hour of Day")
    plt.xlabel("Hour (24h)")
    plt.ylabel("Departure Delay (min)")
    plt.savefig("plots/departure_delay_by_hour.png", dpi=500)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df,
        x="month",
        y="departure_delay",
        estimator=lambda x: sum(x) / len(x),
        errorbar=None,
    )
    plt.title("Average Departure Delay by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Delay (min)")
    plt.savefig("plots/average_delay_by_month.png", dpi=500)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df,
        x="day_of_week",
        y="departure_delay",
        estimator=lambda x: sum(x) / len(x),
        errorbar=None,
    )
    plt.title("Average Departure Delay by Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Average Delay (min)")
    plt.savefig("plots/average_delay_by_day_of_week.png", dpi=500)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x="distance", y="departure_delay", alpha=0.6)
    plt.title("Departure Delay vs. Distance")
    plt.xlabel("Distance (miles)")
    plt.ylabel("Delay (min)")
    plt.savefig("plots/delay_vs_distance.png", dpi=500)
    plt.close()

    plt.figure(figsize=(12, 5))
    sns.countplot(
        data=df,
        x="weather_desc",
        order=df["weather_desc"].value_counts().index,
    )
    plt.title("Flight Count by Weather Condition")
    plt.ylabel("Number of Flights")
    plt.xlabel("Weather Condition")
    plt.xticks(rotation=45)
    plt.savefig("plots/flight_count_by_weather_condition.png", dpi=500)
    plt.close()

    plt.figure(figsize=(12, 14))
    sns.barplot(
        data=df,
        x="weather_desc",
        y="departure_delay",
        estimator=lambda x: sum(x) / len(x),
        errorbar=None,
    )
    plt.title("Average Departure Delay by Weather Condition")
    plt.xlabel("Weather Condition")
    plt.ylabel("Average Delay (min)")
    plt.xticks(rotation=45)
    plt.savefig("plots/average_delay_by_weather_condition.png", dpi=500)
    plt.close()

    print("Plots saved to 'plots/' directory")
