from datetime import datetime

import holidays
import numpy as np
import pandas as pd

US_HOLIDAYS = holidays.US(years=range(2014, 2025))


def convert_time_to_minutes(time_val):
    if pd.isna(time_val):
        return np.nan
    h, m = divmod(int(time_val), 100)
    return h * 60 + m


def label_delay(delay_val):
    if pd.isna(delay_val):
        return np.nan
    return "delayed" if delay_val > 0 else "not_delayed"


def get_season(month):
    if pd.isna(month):
        return np.nan
    month = int(month)
    return (
        "winter"
        if month in [12, 1, 2]
        else "spring"
        if month in [3, 4, 5]
        else "summer"
        if month in [6, 7, 8]
        else "fall"
    )


def is_holiday_or_weekend(row):
    try:
        date = datetime(int(row["year"]), int(row["month"]), int(row["day"]))
        return int(date in US_HOLIDAYS or int(row["day_of_week"]) in [6, 7])
    except Exception:
        return 0


def get_day_of_year(row):
    try:
        return (
            datetime(int(row["year"]), int(row["month"]), int(row["day"]))
            .timetuple()
            .tm_yday
        )
    except Exception:
        return np.nan


def merge_with_weather(flight_df, weather_path):
    weather_df = pd.read_csv(weather_path)
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])

    flight_df["flight_datetime"] = pd.to_datetime(
        flight_df[["year", "month", "day"]]
    ) + pd.to_timedelta(flight_df["dep_min"], unit="minutes")

    weather_df = weather_df.sort_values("datetime").reset_index(drop=True)
    flight_df = flight_df.sort_values("flight_datetime").reset_index(drop=True)

    merged_data = []

    print("Merging flight data with weather data...")
    for idx, flight_row in flight_df.iterrows():
        flight_time = flight_row["flight_datetime"]

        time_diff = abs(weather_df["datetime"] - flight_time)
        closest_idx = time_diff.idxmin()

        if time_diff.iloc[closest_idx] <= pd.Timedelta(hours=2):
            weather_row = weather_df.iloc[closest_idx]

            combined_row = flight_row.copy()

            weather_cols_to_add = [
                "temperature",
                "wind_direction",
                "wind_speed",
                "altimeter",
                "pressure",
                "precipitation",
                "visibility",
                "cloud_height",
                "temperature_celsius",
                "freezing_conditions",
                "wind_speed_category",
                "crosswind_component",
                "visibility_category",
                "cloud_coverage_score",
                "ceiling_height",
                "ifr_conditions",
                "mvfr_conditions",
                "has_precipitation",
                "precipitation_category",
                "low_pressure",
                "pressure_category",
            ]

            weather_cols_to_add.extend(
                [col for col in weather_df.columns if col.startswith("weather_")]
            )

            for col in weather_cols_to_add:
                if col in weather_df.columns:
                    combined_row[col] = weather_row[col]

            merged_data.append(combined_row)

        if idx % 10000 == 0:
            print(f"Processed {idx:,} flight records...")

    merged_df = pd.DataFrame(merged_data)
    print(f"Successfully merged {len(merged_df):,} records")

    return merged_df


def preprocess_flight_data(
    input_path, output_path, weather_path="dataset/processed/jfk_weather_processed.csv"
):
    df = pd.read_csv(input_path)

    # Rename day_of_month to day for pd.to_datetime compatibility
    df = df.rename(columns={"day_of_month": "day"})

    essential_int_cols = [
        "year",
        "month",
        "day",
        "day_of_week",
        "scheduled_departure_time",
        "departure_delay",
    ]
    for col in essential_int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    essential_cols = [
        "year",
        "month",
        "day",
        "scheduled_departure_time",
        "departure_delay",
        "carrier",
    ]
    df.dropna(subset=essential_cols, inplace=True)

    df["label"] = df["departure_delay"].apply(label_delay)
    df["dep_min"] = df["scheduled_departure_time"].apply(convert_time_to_minutes)
    df["dep_sin"] = np.sin(2 * np.pi * df["dep_min"] / 1440)
    df["dep_cos"] = np.cos(2 * np.pi * df["dep_min"] / 1440)

    df["departure_bin"] = pd.cut(
        df["dep_min"],
        bins=[0, 360, 720, 1080, 1440],
        labels=["night", "morning", "afternoon", "evening"],
        include_lowest=True,
        right=False,
    )

    df["day_of_year"] = df.apply(get_day_of_year, axis=1)
    df["days_in_year"] = df["year"].apply(
        lambda y: 366 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 365
    )
    df["day_of_year_sin"] = np.sin(2 * np.pi * df["day_of_year"] / df["days_in_year"])
    df["day_of_year_cos"] = np.cos(2 * np.pi * df["day_of_year"] / df["days_in_year"])

    df["season"] = df["month"].apply(get_season)
    df["is_holiday_or_weekend"] = df.apply(is_holiday_or_weekend, axis=1).astype(bool)

    df["part_of_month_early"] = (df["day"] <= 10).astype(bool)
    df["part_of_month_mid"] = ((df["day"] > 10) & (df["day"] <= 20)).astype(bool)
    df["part_of_month_late"] = (df["day"] > 20).astype(bool)

    df = merge_with_weather(df, weather_path)

    for col in ["month", "day_of_week", "carrier", "departure_bin", "season"]:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=False, dtype=bool)
            df = pd.concat([df, dummies], axis=1)

    final_cols = [
        "scheduled_elapsed_time",
        "label",
        "dep_min",
        "dep_sin",
        "dep_cos",
        "day_of_year_sin",
        "day_of_year_cos",
        "part_of_month_early",
        "part_of_month_mid",
        "part_of_month_late",
        "is_holiday_or_weekend",
    ]

    for prefix in ["month_", "day_of_week_", "carrier_", "departure_bin_", "season_"]:
        final_cols.extend([col for col in df.columns if col.startswith(prefix)])

    weather_cols = [
        "temperature",
        "wind_direction",
        "wind_speed",
        "altimeter",
        "pressure",
        "precipitation",
        "visibility",
        "cloud_height",
        "temperature_celsius",
        "freezing_conditions",
        "wind_speed_category",
        "crosswind_component",
        "visibility_category",
        "cloud_coverage_score",
        "ceiling_height",
        "ifr_conditions",
        "mvfr_conditions",
        "has_precipitation",
        "precipitation_category",
        "low_pressure",
        "pressure_category",
    ]

    weather_cols.extend([col for col in df.columns if col.startswith("weather_")])

    final_cols.extend([col for col in weather_cols if col in df.columns])

    df[final_cols].to_csv(output_path, index=False)
    print(f"✅ Combined flight and weather data saved to {output_path}")
    print(f"Final dataset shape: {df[final_cols].shape}")
