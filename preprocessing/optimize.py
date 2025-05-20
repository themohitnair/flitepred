from datetime import datetime

import holidays
import numpy as np
import pandas as pd

# Build US holiday calendar for 2014–2024
US_HOLIDAY_CAL = holidays.US(years=range(2014, 2025))


def convert_time_to_minutes(t):
    """Convert HHMM integer to minutes since midnight"""
    h = t // 100
    m = t % 100
    return h * 60 + m


def label_delay(x):
    """Classify delay into early, ontime, delayed"""
    if x < 0:
        return "early"
    elif x <= 15:
        return "ontime"
    else:
        return "delayed"


def get_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def is_holiday_or_weekend(row):
    try:
        date = datetime(
            year=int(row["year"]), month=int(row["month"]), day=int(row["day_of_month"])
        )
    except ValueError:
        return 0
    return int(date in US_HOLIDAY_CAL or row["day_of_week"] in [6, 7])


def preprocess_flight_data(
    input_path="dataset/processed/airline_filtered_pruned.csv",
    output_path="dataset/processed/jfk_optimized.csv",
):
    df = pd.read_csv(input_path)

    # --- Target Label ---
    df["label"] = df["departure_delay"].apply(label_delay)

    # --- Time Features ---
    df["dep_min"] = df["scheduled_departure_time"].apply(convert_time_to_minutes)
    df["dep_sin"] = np.sin(2 * np.pi * df["dep_min"] / 1440)
    df["dep_cos"] = np.cos(2 * np.pi * df["dep_min"] / 1440)

    # --- Binning Time ---
    df["departure_bin"] = pd.cut(
        df["dep_min"],
        bins=[0, 360, 720, 1080, 1440],
        labels=["night", "morning", "afternoon", "evening"],
        right=False,
    )

    # --- Day Period ---
    df["day_period"] = pd.cut(
        df["day_of_month"],
        bins=[0, 10, 20, 31],
        labels=["early", "mid", "late"],
        right=False,
    )

    # --- Season ---
    df["season"] = df["month"].apply(get_season)

    # --- Holiday / Weekend ---
    df["is_holiday_or_weekend"] = df.apply(is_holiday_or_weekend, axis=1)

    # --- Sort by Date ---
    df = df.sort_values(by=["year", "month", "day_of_month", "dep_min"]).reset_index(
        drop=True
    )

    # --- Drop Raw Time / Delay ---
    df = df.drop(columns=["scheduled_departure_time", "departure_delay", "year"])

    # --- One-hot Encoding ---
    df = pd.get_dummies(
        df,
        columns=[
            "month",
            "day_of_week",
            "carrier",
            "departure_bin",
            "day_period",
            "season",
        ],
    )

    # --- Save to CSV ---
    df.to_csv(output_path, index=False)
    print(f"✅ Processed data saved to {output_path}")

    return df
