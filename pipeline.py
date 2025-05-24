from preprocessing.amalgamate import amalgamate_flight_data
from preprocessing.filter import filter_selected_carriers_and_destination
from preprocessing.optimize import preprocess_flight_data
from preprocessing.prune import prune_flight_data
from preprocessing.stats import (
    analyze_flight_statistics,
    check_class_imbalance_from_csv,
)

if __name__ == "__main__":
    amalgamate_flight_data(
        raw_data_path="dataset/raw", output_file="dataset/processed/jfk_combined.csv"
    )

    analyze_flight_statistics()
    filter_selected_carriers_and_destination()
    prune_flight_data()
    preprocess_flight_data(
        input_path="dataset/processed/airline_filtered_pruned.csv",
        output_path="dataset/processed/jfk_optimized.csv",
    )
    check_class_imbalance_from_csv()
