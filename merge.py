import pandas as pd
import os


def load_data():
    weather_path = "dataset/processed_data/weather_cleaned.csv"
    flights_path = "dataset/processed_data/filtered_flights.csv"

    print(f"Loading weather data from {weather_path}")
    weather_df = pd.read_csv(weather_path, low_memory=False)
    print(f"Weather data shape: {weather_df.shape}")

    print(f"Loading flights data from {flights_path}")
    flights_df = pd.read_csv(flights_path, low_memory=False)
    print(f"Flights data shape: {flights_df.shape}")

    print("\nWeather data columns and types:")
    for col in weather_df.columns:
        print(f"{col}: {weather_df[col].dtype}")

        missing = weather_df[col].isna().sum()
        if missing > 0:
            print(
                f"  - Missing values: {missing}/{len(weather_df)} ({missing / len(weather_df) * 100:.2f}%)"
            )

    print("\nFlights data columns and types:")
    for col in flights_df.columns:
        print(f"{col}: {flights_df[col].dtype}")

        missing = flights_df[col].isna().sum()
        if missing > 0:
            print(
                f"  - Missing values: {missing}/{len(flights_df)} ({missing / len(flights_df) * 100:.2f}%)"
            )

    return weather_df, flights_df


def process_weather_data(weather_df):
    weather_df["TIME"] = weather_df["TIME"].astype(str).str.zfill(4)
    weather_df["HOUR"] = weather_df["TIME"].str[:2].astype(int)
    weather_df["MINUTE"] = weather_df["TIME"].str[2:].astype(int)

    required_cols = ["YEAR", "MONTH", "DAY_OF_MONTH", "HOUR", "MINUTE"]
    weather_df = weather_df.dropna(subset=required_cols)

    weather_df["YEAR"] = weather_df["YEAR"].astype(int)
    weather_df["MONTH"] = weather_df["MONTH"].astype(int)
    weather_df["DAY_OF_MONTH"] = weather_df["DAY_OF_MONTH"].astype(int)

    try:
        weather_df["DATETIME"] = pd.to_datetime(
            {
                "year": weather_df["YEAR"],
                "month": weather_df["MONTH"],
                "day": weather_df["DAY_OF_MONTH"],
                "hour": weather_df["HOUR"],
                "minute": weather_df["MINUTE"],
            }
        )
    except Exception as e:
        print(f"Error creating datetime objects: {e}")
        print("Sample of problematic data:")
        print(weather_df[required_cols].head())
        raise

    return weather_df


def process_flights_data(flights_df):
    required_cols = ["YEAR", "MONTH", "DAY_OF_MONTH", "CRS_DEP_TIME"]
    flights_df = flights_df.dropna(subset=required_cols)

    # Ensure date columns are integers
    flights_df["YEAR"] = flights_df["YEAR"].astype(int)
    flights_df["MONTH"] = flights_df["MONTH"].astype(int)
    flights_df["DAY_OF_MONTH"] = flights_df["DAY_OF_MONTH"].astype(int)

    if "DEP_TIME" in flights_df.columns and pd.api.types.is_datetime64_dtype(
        flights_df["DEP_TIME"]
    ):
        flights_df["DATETIME"] = flights_df["DEP_TIME"]
    else:
        flights_df["CRS_DEP_TIME"] = flights_df["CRS_DEP_TIME"].astype(str).str.zfill(4)
        flights_df["HOUR"] = flights_df["CRS_DEP_TIME"].str[:2].astype(int)
        flights_df["MINUTE"] = flights_df["CRS_DEP_TIME"].str[2:].astype(int)

        try:
            flights_df["DATETIME"] = pd.to_datetime(
                {
                    "year": flights_df["YEAR"],
                    "month": flights_df["MONTH"],
                    "day": flights_df["DAY_OF_MONTH"],
                    "hour": flights_df["HOUR"],
                    "minute": flights_df["MINUTE"],
                }
            )
        except Exception as e:
            print(f"Error creating datetime objects for flights: {e}")
            print("Sample of problematic data:")
            print(
                flights_df[["YEAR", "MONTH", "DAY_OF_MONTH", "HOUR", "MINUTE"]].head()
            )
            raise

    return flights_df


def find_closest_weather_data(flights_df, weather_df):
    merged_df = flights_df.copy()

    merged_df["closest_weather_idx"] = None
    merged_df["time_diff_minutes"] = None

    for idx, flight in flights_df.iterrows():
        flight_time = flight["DATETIME"]

        same_day_weather = weather_df[
            (weather_df["YEAR"] == flight["YEAR"])
            & (weather_df["MONTH"] == flight["MONTH"])
            & (weather_df["DAY_OF_MONTH"] == flight["DAY_OF_MONTH"])
        ]

        if len(same_day_weather) == 0:
            continue

        time_diffs = abs(
            (same_day_weather["DATETIME"] - flight_time).dt.total_seconds() / 60
        )

        closest_idx = time_diffs.idxmin()
        min_diff = time_diffs.min()

        merged_df.at[idx, "closest_weather_idx"] = closest_idx
        merged_df.at[idx, "time_diff_minutes"] = min_diff

    return merged_df


def merge_datasets(merged_df, weather_df):
    result_df = merged_df.copy()
    if "closest_weather_idx" in result_df.columns:
        weather_columns = [
            "tmpc",
            "dwpc",
            "relh",
            "drct",
            "sknt",
            "alti",
            "p01i",
            "vsby",
            "gust",
            "skyc1",
            "skyl1",
            "ice_accretion_1hr",
            "snowdepth",
        ]

        for col in weather_columns:
            result_df[f"weather_{col}"] = None

        for idx, row in result_df.iterrows():
            if pd.notna(row["closest_weather_idx"]):
                weather_row = weather_df.loc[row["closest_weather_idx"]]
                for col in weather_columns:
                    if col in weather_df.columns:
                        result_df.at[idx, f"weather_{col}"] = weather_row[col]

        result_df.drop(
            ["closest_weather_idx", "time_diff_minutes"], axis=1, inplace=True
        )

    return result_df


def main():
    try:
        print("Loading data...")
        weather_df, flights_df = load_data()

        print("\nProcessing weather data...")
        weather_df = process_weather_data(weather_df)
        print(f"Weather data after processing: {weather_df.shape}")

        print("\nProcessing flights data...")
        flights_df = process_flights_data(flights_df)
        print(f"Flights data after processing: {flights_df.shape}")

        print("\nFinding closest weather data for each flight...")
        merged_df = find_closest_weather_data(flights_df, weather_df)
        print(f"Merged data shape: {merged_df.shape}")

        print("\nMerging datasets...")
        result_df = merge_datasets(merged_df, weather_df)
        print(f"Final result shape: {result_df.shape}")

        output_dir = "dataset/processed_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, "merged_flights_weather.csv")
        result_df.to_csv(output_path, index=False)

        print(f"\nMerged dataset saved to {output_path}")
        print(f"Total flights: {len(flights_df)}")
        print(f"Total weather observations: {len(weather_df)}")
        print(f"Total merged records: {len(result_df)}")

        print("\nSample of merged data:")
        print(result_df.head())

        if "time_diff_minutes" in merged_df.columns:
            print("\nTime difference distribution (minutes):")
            print(f"Min: {merged_df['time_diff_minutes'].min()}")
            print(f"Max: {merged_df['time_diff_minutes'].max()}")
            print(f"Mean: {merged_df['time_diff_minutes'].mean()}")
            print(f"Median: {merged_df['time_diff_minutes'].median()}")

    except Exception as e:
        print(f"\nError in main process: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
