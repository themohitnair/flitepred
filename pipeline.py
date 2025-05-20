from preprocessing.amalgamate import amalgamate_flight_data
from preprocessing.filter import filter_selected_carriers_and_destination
from preprocessing.stats import analyze_flight_statistics

if __name__ == "__main__":
    amalgamate_flight_data(
        raw_data_path="dataset/raw", output_file="dataset/jfk_combined.csv"
    )
    analyze_flight_statistics()
    filter_selected_carriers_and_destination()
