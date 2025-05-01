import pandas as pd
from pathlib import Path
from datetime import datetime


def process_year_data(year_dir):
    print(f"\nProcessing data for {year_dir.name}")

    csv_files = sorted(year_dir.glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files for {year_dir.name}")

    if not csv_files:
        print(f"No CSV files found in {year_dir}")
        return None

    print("Combining CSV files...")
    df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    print(f"Combined data shape: {df.shape}")

    print("\nFiltering by origin airport (12478)")
    initial_count = len(df)
    df = df[df["ORIGIN_AIRPORT_ID"] == 12478]
    filtered_count = len(df)
    print(f"Filtered out {initial_count - filtered_count} rows")
    print(f"Remaining rows: {filtered_count}")

    print("\nRemoving cancelled and diverted flights")
    initial_count = len(df)
    df = df[(df["CANCELLED"] == 0) & (df["DIVERTED"] == 0)]
    filtered_count = len(df)
    print(f"Filtered out {initial_count - filtered_count} rows")
    print(f"Remaining rows: {filtered_count}")

    print("\nRemoving rows with missing values")
    initial_count = len(df)
    df = df.dropna()
    filtered_count = len(df)
    print(f"Filtered out {initial_count - filtered_count} rows")
    print(f"Remaining rows: {filtered_count}")

    print("\nRemoving unnecessary columns: ORIGIN_AIRPORT_ID, CANCELLED, DIVERTED")
    columns_to_remove = ["ORIGIN_AIRPORT_ID", "CANCELLED", "DIVERTED"]
    df = df.drop(columns=columns_to_remove)
    print(f"Removed {len(columns_to_remove)} columns")
    print(f"Remaining columns: {', '.join(df.columns)}")

    return df


def main():
    dataset_dir = Path("dataset/raw")
    output_dir = Path("dataset/processed_data/yearwise")
    output_dir.mkdir(exist_ok=True)

    year_dirs = sorted([d for d in dataset_dir.iterdir() if d.is_dir()])

    for year_dir in year_dirs:
        df = process_year_data(year_dir)
        if df is not None and not df.empty:
            output_path = output_dir / f"{year_dir.name}_processed.csv"
            df.to_csv(output_path, index=False)
            print(f"\nSaved processed data to {output_path}")
            print(f"Final data shape: {df.shape}")
            print("-" * 50)


if __name__ == "__main__":
    print("Starting data processing pipeline...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
