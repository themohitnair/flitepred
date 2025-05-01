import pandas as pd
from pathlib import Path


def combine_and_filter_data():
    input_dir = Path("dataset/processed_data/yearwise")
    all_files = sorted(input_dir.glob("*.csv"))

    print("Combining all CSVs...")
    df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
    print(f"Combined data shape: {df.shape}")

    print("\nFinding top 3 carriers...")
    top_carriers = df["OP_UNIQUE_CARRIER"].value_counts().head(3).index
    print(f"Top 3 carriers: {', '.join(top_carriers)}")

    print("\nFinding top 5 destinations...")
    top_destinations = df["DEST_AIRPORT_ID"].value_counts().head(5).index
    print(f"Top 5 destinations: {', '.join(map(str, top_destinations))}")

    print("\nFiltering by top 3 carriers...")
    initial_count = len(df)
    df = df[df["OP_UNIQUE_CARRIER"].isin(top_carriers)]
    print(f"Filtered out {initial_count - len(df)} rows")
    print(f"Remaining rows: {len(df)}")

    print("\nFiltering by top 5 destinations...")
    initial_count = len(df)
    df = df[df["DEST_AIRPORT_ID"].isin(top_destinations)]
    print(f"Filtered out {initial_count - len(df)} rows")
    print(f"Remaining rows: {len(df)}")

    df["DEP_TIME"] = pd.to_datetime(
        df["YEAR"].astype(str)
        + df["MONTH"].astype(str).str.zfill(2)
        + df["DAY_OF_MONTH"].astype(str).str.zfill(2)
        + df["CRS_DEP_TIME"].astype(str).str.zfill(4),
        format="%Y%m%d%H%M",
    )
    df = df.sort_values("DEP_TIME")

    output_dir = Path("dataset/processed_data")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "filtered_flights.csv"

    print(f"\nSaving filtered data to {output_path}")
    df.to_csv(output_path, index=False)
    print(f"Final data shape: {df.shape}")


if __name__ == "__main__":
    combine_and_filter_data()
