from datetime import datetime

import holidays
import numpy as np
import pandas as pd

US_HOLIDAYS = holidays.US(years=range(2014, 2025))


def convert_time_to_minutes(time_val):
    """Convert HHMM to minutes since midnight."""
    if pd.isna(time_val):
        return np.nan
    h, m = divmod(int(time_val), 100)
    return h * 60 + m


def label_delay(delay_val):
    """Label flight as delayed or not_delayed."""
    if pd.isna(delay_val):
        return np.nan
    return "delayed" if delay_val > 0 else "not_delayed"


def get_season(month):
    """Return season name based on month."""
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
    """Check if the date is a holiday or a weekend."""
    try:
        date = datetime(int(row["year"]), int(row["month"]), int(row["day_of_month"]))
        return int(date in US_HOLIDAYS or int(row["day_of_week"]) in [6, 7])
    except Exception:
        return 0


def get_day_of_year(row):
    """Get the day of year for the given date."""
    try:
        return (
            datetime(int(row["year"]), int(row["month"]), int(row["day_of_month"]))
            .timetuple()
            .tm_yday
        )
    except Exception:
        return np.nan


def preprocess_flight_data(input_path, output_path):
    df = pd.read_csv(input_path)

    essential_int_cols = [
        "year",
        "month",
        "day_of_month",
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
        "day_of_month",
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

    df["part_of_month_early"] = (df["day_of_month"] <= 10).astype(bool)
    df["part_of_month_mid"] = (
        (df["day_of_month"] > 10) & (df["day_of_month"] <= 20)
    ).astype(bool)
    df["part_of_month_late"] = (df["day_of_month"] > 20).astype(bool)

    for col in ["month", "day_of_week", "carrier", "departure_bin", "season"]:
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

    df[final_cols].to_csv(output_path, index=False)
