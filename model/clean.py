import pandas as pd


def clean_flight_data(input_file, output_file):
    df = pd.read_csv(input_file)

    df["Month"] = pd.to_datetime(df["Used Date"], format="%d-%m-%Y").dt.month

    df.rename(
        columns={
            "weather__hourly__windspeedKmph": "Windspeed",
            "weather__hourly__weatherDesc__value": "WeatherDescription",
            "weather__hourly__precipMM": "Precipitation",
            "weather__hourly__humidity": "Humidity",
            "weather__hourly__visibility": "Visibility",
            "weather__hourly__pressure": "Pressure",
            "weather__hourly__cloudcover": "Cloudcover",
        },
        inplace=True,
    )

    columns_to_keep = [
        "Month",
        "From",
        "To",
        "Airline",
        "SDEP",
        "DEP",
        "SARR",
        "ARR",
        "Distance",
        "Passenger Load Factor",
        "Market Share",
        "Windspeed",
        "WeatherDescription",
        "Precipitation",
        "Humidity",
        "Visibility",
        "Pressure",
        "Cloudcover",
        "Departure Delay",
    ]
    df = df[columns_to_keep]

    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV saved as {output_file}")


if __name__ == "__main__":
    clean_flight_data("dataset/raw_flight_data.csv", "dataset/flight_data.csv")
