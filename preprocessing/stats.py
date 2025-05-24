from pathlib import Path
from typing import Union

import pandas as pd


def analyze_flight_statistics(
    data_file: Union[str, Path] = "dataset/processed/jfk_combined.csv",
) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """
    Analyzes flight data and returns the top 5 destinations, airline carriers,
    and airline+destination route combinations.

    Parameters:
    -----------
    data_file : str or Path
        Path to the combined CSV file to analyze

    Returns:
    --------
    tuple
        (top_5_destinations, top_5_carriers, top_5_routes)
        - top_5_destinations: pd.Series
        - top_5_carriers: pd.Series
        - top_5_routes: pd.DataFrame with columns ['Carrier', 'Destination', 'Flight Count']
    """
    df = pd.read_csv(data_file)

    top_5_destinations = df["DEST_AIRPORT_ID"].value_counts().head(5)

    top_5_carriers = df["OP_UNIQUE_CARRIER"].value_counts().head(5)

    route_counts = (
        df.groupby(["OP_UNIQUE_CARRIER", "DEST_AIRPORT_ID"])
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Flight Count")
        .rename(
            columns={"OP_UNIQUE_CARRIER": "Carrier", "DEST_AIRPORT_ID": "Destination"}
        )
        .head(10)
    )

    print("Top 5 Destinations:\n", top_5_destinations)
    print("\nTop 5 Airline Carriers:\n", top_5_carriers)
    print("\nTop 5 Routes (Carrier + Destination):\n", route_counts)

    return top_5_destinations, top_5_carriers, route_counts


def check_class_imbalance_from_csv(
    csv_path="dataset/processed/jfk_optimized.csv", target_col="label"
):
    df = pd.read_csv(csv_path)
    counts = df[target_col].value_counts()
    percentages = df[target_col].value_counts(normalize=True) * 100
    print(f"Class distribution for '{target_col}':\n")
    print("Counts:")
    print(counts)
    print("\nPercentages:")
    print(percentages)
