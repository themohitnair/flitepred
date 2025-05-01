import pandas as pd
from pathlib import Path


def verify_data():
    df = pd.read_csv(Path("dataset/processed_data/filtered_flights.csv"))

    print("\nVerifying Airline Carriers:")
    carrier_counts = df["OP_UNIQUE_CARRIER"].value_counts()
    print(f"Number of unique carriers: {len(carrier_counts)}")
    print("\nCarrier frequencies:")
    for carrier, count in carrier_counts.items():
        print(f"{carrier}: {count} flights")

    print("\n\nVerifying Destinations:")
    destination_counts = df["DEST_AIRPORT_ID"].value_counts()
    print(f"Number of unique destinations: {len(destination_counts)}")
    print("\nDestination frequencies:")
    for dest, count in destination_counts.items():
        print(f"{dest}: {count} flights")

    print("\n\nVerifying Routes:")
    routes = df.groupby(["OP_UNIQUE_CARRIER", "DEST_AIRPORT_ID"]).size()
    print(f"Number of unique routes: {len(routes)}")
    print("\nRoute frequencies:")
    for (carrier, dest), count in routes.items():
        print(f"{carrier} -> {dest}: {count} flights")


if __name__ == "__main__":
    verify_data()
