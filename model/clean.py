import pandas as pd


def clean_flight_data(input_file, output_file):
    df = pd.read_csv(input_file)

    # Convert date to datetime format
    df["Used_Date_DT"] = pd.to_datetime(df["Used Date"], format="%d-%m-%Y")

    # Extract month and day of week (1-7 where 1 is Monday)
    df["Month"] = df["Used_Date_DT"].dt.month
    df["Day Of Week"] = (
        df["Used_Date_DT"].dt.dayofweek + 1
    )  # Adding 1 to make it 1-7 instead of 0-6

    # You could also add a "Season" feature
    # df["Season"] = df["Month"].apply(lambda x: 1 if x in [12, 1, 2] else 2 if x in [3, 4, 5] else 3 if x in [6, 7, 8] else 4)

    df.rename(
        columns={
            "SDEP": "Scheduled Departure Time",
            "weather__hourly__windspeedKmph": "Windspeed",
            "weather__hourly__weatherDesc__value": "Weather Description",
            "weather__hourly__precipMM": "Precipitation",
            "weather__hourly__humidity": "Humidity",
            "weather__hourly__visibility": "Visibility",
            "weather__hourly__pressure": "Pressure",
            "weather__hourly__cloudcover": "Cloud Cover",
        },
        inplace=True,
    )

    columns_to_keep = [
        "Month",
        "Day Of Week",
        "From",
        "To",
        "Airline",
        "Scheduled Departure Time",
        "Distance",
        "Passenger Load Factor",
        "Market Share",
        "Windspeed",
        "Weather Description",
        "Precipitation",
        "Humidity",
        "Visibility",
        "Pressure",
        "Cloud Cover",
        "Departure Delay",
    ]
    df = df[columns_to_keep]

    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV saved as {output_file}")


if __name__ == "__main__":
    clean_flight_data("dataset/raw_flight_data.csv", "dataset/flight_data.csv")
