import pandas as pd
from pathlib import Path


def analyze_data():
    processed_dir = Path("dataset/processed_data")

    all_files = sorted(processed_dir.glob("*.csv"))
    df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

    top_carriers = df["OP_UNIQUE_CARRIER"].value_counts().head(3)
    top_destinations = df["DEST_AIRPORT_ID"].value_counts().head(5)

    print("\nTop 5 Airline Carriers by Frequency:")
    for carrier, count in top_carriers.items():
        print(f"{carrier}: {count} flights")

    print("\nTop 5 Destination Airports by Frequency:")
    for airport, count in top_destinations.items():
        print(f"{airport}: {count} flights")

    print("\nDetailed Route Analysis:")
    for carrier in top_carriers.index:
        print(f"\nRoutes for Carrier {carrier}:")
        carrier_df = df[df["OP_UNIQUE_CARRIER"] == carrier]

        for dest in top_destinations.index:
            route_df = carrier_df[carrier_df["DEST_AIRPORT_ID"] == dest]
            route_count = len(route_df)
            print(f"  {carrier} -> {dest}: {route_count} flights")


if __name__ == "__main__":
    analyze_data()
