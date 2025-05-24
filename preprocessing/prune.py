import os

import pandas as pd


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames columns to human-readable names with all lowercase and underscores, and removes specified columns.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with original column names

    Returns:
    --------
    pd.DataFrame
        Dataframe with renamed columns and specified columns removed
    """
    rename_map = {
        "YEAR": "year",
        "MONTH": "month",
        "DAY_OF_MONTH": "day_of_month",
        "DAY_OF_WEEK": "day_of_week",
        "OP_UNIQUE_CARRIER": "carrier",
        "CRS_DEP_TIME": "scheduled_departure_time",
        "DEP_DELAY": "departure_delay",
        "CANCELLED": "cancelled",
        "DIVERTED": "diverted",
        "CRS_ELAPSED_TIME": "scheduled_elapsed_time",
    }

    df = df.rename(columns=rename_map)

    if "ORIGIN_AIRPORT_ID" in df.columns:
        df = df.drop(columns=["ORIGIN_AIRPORT_ID"])
    if "DEST_AIRPORT_ID" in df.columns:
        df = df.drop(columns=["DEST_AIRPORT_ID"])

    return df


def prune_flight_data(
    input_path: str = "dataset/processed/airline_filtered.csv",
    output_path: str = "dataset/processed/airline_filtered_pruned.csv",
) -> None:
    """
    Prunes the flight dataset by removing cancelled or diverted flights and rows with null values.

    Parameters:
    -----------
    input_path : str
        Path to the input CSV file
    output_path : str
        Path to save the pruned CSV file
    """
    try:
        df = pd.read_csv(input_path)
        print(f"Initial shape: {df.shape}")

        df = df[df["CANCELLED"] == 0.0]

        df = df[df["DIVERTED"] == 0.0]

        df = df.dropna()

        df = df.drop(columns=["CANCELLED", "DIVERTED", "DISTANCE"])

        df = rename_columns(df)

        print(f"Final shape after filtering: {df.shape}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_csv(output_path, index=False)
        print(f"Filtered data saved to {output_path}")
    except FileNotFoundError:
        print(f"File not found. Please check the path: {input_path}")
