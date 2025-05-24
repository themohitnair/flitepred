import pandas as pd

from preprocessing.amalgamate import amalgamate_flight_data
from preprocessing.augment import preprocess_iem_weather_data
from preprocessing.filter import filter_selected_carriers_and_destination
from preprocessing.impute import impute_and_clean_dataset
from preprocessing.optimize import preprocess_flight_data
from preprocessing.prune import prune_flight_data
from preprocessing.stats import (
    analyze_flight_statistics,
)

if __name__ == "__main__":
    amalgamate_flight_data(
        raw_data_path="dataset/raw", output_file="dataset/processed/jfk_combined.csv"
    )

    analyze_flight_statistics()
    filter_selected_carriers_and_destination()
    prune_flight_data()

    df = pd.read_csv("dataset/raw/weather_2014_2024.csv")

    processed_df = preprocess_iem_weather_data(df)

    processed_df.to_csv("dataset/processed/jfk_weather_processed.csv", index=False)
    print("\n✅ Processed weather data saved to 'jfk_weather_processed.csv'")

    preprocess_flight_data(
        input_path="dataset/processed/airline_filtered_pruned.csv",
        output_path="dataset/processed/jfk_optimized.csv",
    )
    file_path = "dataset/processed/jfk_optimized.csv"
    clean_df = impute_and_clean_dataset(file_path)

    # Optional: Quick data quality check
    print("\n=== Data Quality Check ===")
    print("Label distribution:")
    print(clean_df["label"].value_counts())
    print("\nDataset ready for machine learning!")
