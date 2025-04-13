import pandas as pd

df = pd.read_csv("dataset/processed/jfk_final_2024.csv")

carrier_counts = df["airline_carrier"].value_counts()
destination_counts = df["destination_airport_id"].value_counts()

print("Flights per Airline Carrier:")
print(carrier_counts)

print("\nFlights per Destination Airport:")
print(destination_counts)
