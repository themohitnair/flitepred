from pathlib import Path
from typing import Union

import pandas as pd


def filter_selected_carriers_and_destination(
    data_file: Union[str, Path] = "dataset/processed/jfk_combined.csv",
    carriers: list[str] = ["AA", "B6", "DL"],
    destination: int = 12892,
    output_file: Union[str, Path] = "dataset/processed/airline_filtered.csv",
) -> pd.DataFrame:
    """
    Filters the dataset by selected airline carriers and destination airport ID,
    and saves the filtered dataset.

    Parameters:
    -----------
    data_file : str or Path
        Path to the CSV file.
    carriers : list of str
        Airline carrier codes to filter by.
    destination : int
        Destination airport ID to filter by.
    output_file : str or Path
        Path where the filtered CSV should be saved.

    Returns:
    --------
    pd.DataFrame
        Filtered DataFrame.
    """
    df = pd.read_csv(data_file)

    filtered_df = df[
        (df["OP_UNIQUE_CARRIER"].isin(carriers))
        & (df["DEST_AIRPORT_ID"] == destination)
    ]

    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save filtered data
    filtered_df.to_csv(output_file, index=False)

    print(
        f"Filtered {len(filtered_df)} rows for carriers {carriers} and destination {destination}"
    )
    print(f"Saved to: {output_file}")

    return filtered_df
