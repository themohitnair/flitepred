from datetime import datetime

import holidays
import numpy as np
import pandas as pd

# Build US holiday calendar for 2014–2024 (Assuming this is already in your script)
US_HOLIDAY_CAL = holidays.US(years=range(2014, 2025))


# Assuming these helper functions are defined in your script:
def convert_time_to_minutes(t):
    """Convert HHMM integer to minutes since midnight"""
    if pd.isna(t):  # Handle potential NaNs if CRS_DEP_TIME can be missing
        return np.nan
    h = int(t) // 100
    m = int(t) % 100
    return h * 60 + m


def label_delay(x):
    """Binary classification: delayed or not"""
    if pd.isna(x):  # Handle potential NaNs if DEP_DELAY can be missing
        return np.nan
    if x > 0:
        return "delayed"
    else:
        return "not_delayed"


def get_season(month):
    if pd.isna(month):
        return np.nan  # Handle potential NaNs
    month = int(month)
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:  # months 9, 10, 11
        return "fall"


def is_holiday_or_weekend(row):
    try:
        # Ensure year, month, day_of_month are valid integers before creating datetime
        year = int(row["year"])
        month = int(row["month"])
        day = int(row["day_of_month"])
        date = datetime(year=year, month=month, day=day)
        # Ensure day_of_week is a valid number for comparison
        day_of_week = int(row["day_of_week"])
        return int(
            date in US_HOLIDAY_CAL or day_of_week in [6, 7]
        )  # Assuming day_of_week: 1=Mon, 7=Sun
    except (
        ValueError,
        TypeError,
    ):  # Catch errors if date components are invalid or NaN
        return 0


def preprocess_flight_data(
    input_path="dataset/processed/airline_filtered_pruned.csv",
    output_path="dataset/processed/jfk_optimized.csv",
):
    df = pd.read_csv(input_path)

    # --- Ensure correct data types for critical columns at the start ---
    # These are columns used in calculations or datetime conversions.
    # Adjust column names if they are different in your input CSV.
    cols_to_numeric_int = [
        "year",
        "month",
        "day_of_month",
        "day_of_week",
        "scheduled_departure_time",
    ]
    for col in cols_to_numeric_int:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )  # Coerce errors to NaT/NaN

    if "departure_delay" in df.columns:
        df["departure_delay"] = pd.to_numeric(df["departure_delay"], errors="coerce")

    # Drop rows where essential identifiers or target-related features are NaN after conversion
    # This is important before proceeding with feature engineering
    essential_cols_for_dropna = [
        "year",
        "month",
        "day_of_month",
        "scheduled_departure_time",
        "departure_delay",
        "carrier",
    ]
    # Filter out columns that might not be present, though they should be
    essential_cols_for_dropna = [
        col for col in essential_cols_for_dropna if col in df.columns
    ]
    df.dropna(subset=essential_cols_for_dropna, inplace=True)

    # --- Target Label ---
    df["label"] = df["departure_delay"].apply(label_delay)

    # --- Time Features ---
    df["dep_min"] = df["scheduled_departure_time"].apply(convert_time_to_minutes)
    df["dep_sin"] = np.sin(2 * np.pi * df["dep_min"] / 1440)
    df["dep_cos"] = np.cos(2 * np.pi * df["dep_min"] / 1440)

    # --- Binning Time ---
    df["departure_bin"] = pd.cut(
        df["dep_min"],
        bins=[0, 360, 720, 1080, 1440],  # 0-6 AM, 6 AM-12 PM, 12 PM-6 PM, 6 PM-12 AM
        labels=["night", "morning", "afternoon", "evening"],
        right=False,
        include_lowest=True,  # Ensure 0 is included
    )

    # --- ⭐ New Features Start Here ⭐ ---

    # 1. Cyclical Day of Year (day_of_year_sin, day_of_year_cos)
    # Ensure year, month, day_of_month are integer type for datetime
    df["year"] = df["year"].astype(int)
    df["month"] = df["month"].astype(int)
    df["day_of_month"] = df["day_of_month"].astype(int)

    def get_day_of_year(row):
        try:
            return (
                datetime(row["year"], row["month"], row["day_of_month"])
                .timetuple()
                .tm_yday
            )
        except ValueError:
            return np.nan  # Should not happen if NaN rows were dropped

    df["day_of_year"] = df.apply(get_day_of_year, axis=1)

    def is_leap(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    df["days_in_year"] = df["year"].apply(lambda y: 366 if is_leap(y) else 365)

    df["day_of_year_sin"] = np.sin(2 * np.pi * df["day_of_year"] / df["days_in_year"])
    df["day_of_year_cos"] = np.cos(2 * np.pi * df["day_of_year"] / df["days_in_year"])

    # 2. Seasonal Features
    df["season"] = df["month"].apply(get_season)

    # 3. Part of Month Features
    df["part_of_month_early"] = (
        (df["day_of_month"] >= 1) & (df["day_of_month"] <= 10)
    ).astype(int)
    df["part_of_month_mid"] = (
        (df["day_of_month"] >= 11) & (df["day_of_month"] <= 20)
    ).astype(int)
    df["part_of_month_late"] = (df["day_of_month"] > 20).astype(int)

    # Note: 'dep_min' will be kept (removed from the drop list below).

    # --- ⭐ New Features End Here ⭐ ---

    df["day_of_week"] = df["day_of_week"].astype(
        int
    )  # Ensure day_of_week is int for is_holiday_or_weekend
    df["is_holiday_or_weekend"] = df.apply(is_holiday_or_weekend, axis=1)

    # --- Sort by Date ---
    # Sort before dropping 'month', 'day_of_month' if they are used for sorting,
    # but dep_min is usually the finest sort key for a given day.
    df = df.sort_values(by=["year", "month", "day_of_month", "dep_min"]).reset_index(
        drop=True
    )

    # --- Drop Raw Time / Intermediate Columns ---
    columns_to_drop = [
        "scheduled_departure_time",  # Original CRS_DEP_TIME
        "departure_delay",  # Original DEP_DELAY
        # "dep_min",                # Keeping dep_min as a feature
        "day_of_year",  # Helper column
        "days_in_year",  # Helper column
        # 'day_of_month' will be dropped if it's not used by anything else
        # and if part_of_month features are sufficient.
        # If you one-hot encode 'month', the original 'month' column is also typically dropped by get_dummies.
        # However, explicitly listing what to drop is clearer.
        # The original script dropped 'day_of_month'. Let's stick to that.
        "day_of_month",
    ]
    # Ensure columns exist before trying to drop them
    actual_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(columns=actual_columns_to_drop)

    # --- One-hot Encoding ---
    # 'month' will be one-hot encoded (e.g., month_1, month_2...).
    # 'day_of_week' will be one-hot encoded.
    # 'carrier' will be one-hot encoded.
    # 'departure_bin' will be one-hot encoded.
    # 'season' (new) will be one-hot encoded (e.g., season_winter, season_spring...).
    columns_to_one_hot = [
        "month",  # This will create month_1, month_2 etc.
        "day_of_week",
        "carrier",
        "departure_bin",
        "season",  # Added new seasonal feature for OHE
    ]
    actual_columns_to_one_hot = [col for col in columns_to_one_hot if col in df.columns]
    df = pd.get_dummies(df, columns=actual_columns_to_one_hot, prefix_sep="_")

    # --- Save to CSV ---
    df.to_csv(output_path, index=False)
    print(f"✅ Processed data saved to {output_path} with {df.shape[1]} columns.")
    print("Final columns:", df.columns.tolist())

    return df
