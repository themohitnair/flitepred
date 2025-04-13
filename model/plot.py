import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")
df = pd.read_csv("dataset/processed/jfk_final_2024.csv")
os.makedirs("plots", exist_ok=True)

plt.figure(figsize=(10, 5))
sns.histplot(df["departure_delay"], bins=50, kde=True)
plt.title("Departure Delay Distribution")
plt.xlabel("Delay (minutes)")
plt.ylabel("Frequency")
plt.savefig("plots/departure_delay_distribution.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.barplot(
    data=df,
    x="airline_carrier",
    y="departure_delay",
    estimator=lambda x: sum(x) / len(x),
)
plt.title("Average Departure Delay by Airline")
plt.ylabel("Average Delay (min)")
plt.savefig("plots/average_delay_by_airline.png")
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
plt.savefig("plots/flight_count_by_destination.png")
plt.close()

plt.figure(figsize=(10, 5))
sns.scatterplot(
    data=df, x="temperature_celsius", y="departure_delay", hue="weather_code", alpha=0.6
)
plt.title("Departure Delay vs. Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Delay (min)")
plt.savefig("plots/delay_vs_temperature.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="weather_code", y="departure_delay")
plt.title("Delays by Weather Code")
plt.xlabel("Weather Code")
plt.ylabel("Departure Delay (min)")
plt.savefig("plots/delays_by_weather_code.png")
plt.close()

plt.figure(figsize=(12, 5))
sns.boxplot(data=df, x="departure_hour", y="departure_delay")
plt.title("Departure Delay by Hour of Day")
plt.xlabel("Hour (24h)")
plt.ylabel("Departure Delay (min)")
plt.savefig("plots/departure_delay_by_hour.png")
plt.close()

print("Plots saved to 'plots/' directory")
