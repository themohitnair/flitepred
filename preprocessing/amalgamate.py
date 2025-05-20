from pathlib import Path
from typing import Union

import pandas as pd


def collect_csv_files(root: Union[str, Path], exclude: list[str] = []) -> list[Path]:
    """Recursively collects all CSVs under `root`, excluding any filenames in `exclude`."""
    root = Path(root)
    return sorted(
        [
            path
            for path in root.rglob("*.csv")
            if path.name not in exclude and path.name.endswith(".csv")
        ]
    )


def load_and_filter_csv(file_path: Path, origin_id: int = 12478) -> pd.DataFrame:
    """Loads a CSV and filters it by ORIGIN_AIRPORT_ID == origin_id."""
    df = pd.read_csv(file_path)
    if "ORIGIN_AIRPORT_ID" in df.columns:
        return df[df["ORIGIN_AIRPORT_ID"] == origin_id]
    return pd.DataFrame()  # empty fallback


def amalgamate_flight_data(
    raw_data_path: Union[str, Path], output_file: Union[str, Path]
):
    """Combines all filtered CSVs into a single file."""
    csv_files = collect_csv_files(raw_data_path, exclude=["jfk_weather_2014_24.csv"])
    print(f"Found {len(csv_files)} CSV files.")

    all_dataframes = [load_and_filter_csv(file) for file in csv_files]
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    print(f"Total records after filtering: {len(combined_df)}")

    combined_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")
