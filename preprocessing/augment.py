import re

import numpy as np
import pandas as pd


def preprocess_iem_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {
        "valid": "datetime",
        "tmpc": "temperature",
        "drct": "wind_direction",
        "sknt": "wind_speed",
        "alti": "altimeter",
        "mslp": "pressure",
        "p01i": "precipitation",
        "vsby": "visibility",
        "skyc1": "cloud_cover",
        "skyl1": "cloud_height",
        "metar": "metar_report",
    }

    df = df.rename(columns=rename_dict)
    df["datetime"] = pd.to_datetime(df["datetime"])

    initial_count = len(df)
    df = df[~df["datetime"].dt.year.isin([2020, 2021])]
    removed_count = initial_count - len(df)
    print(f"Removed {removed_count:,} records from 2020-2021")

    columns_to_drop = [
        "station",
        "skyc2",
        "skyc3",
        "skyl2",
        "skyl3",
        "ice_accretion_1hr",
        "ice_accretion_3hr",
        "ice_accretion_6hr",
    ]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    def clean_numeric_column(series, trace_value=0.001):
        if series.name == "precipitation":
            series = series.replace("T", trace_value)
        series = series.replace("M", np.nan)
        return pd.to_numeric(series, errors="coerce")

    numeric_columns = [
        "temperature",
        "wind_direction",
        "wind_speed",
        "altimeter",
        "pressure",
        "precipitation",
        "visibility",
        "cloud_height",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = clean_numeric_column(df[col])

    if "cloud_cover" in df.columns:
        df["cloud_cover"] = df["cloud_cover"].replace("M", np.nan)

    df = extract_weather_type_from_metar(df)
    df = add_weather_features(df)

    intermediate_columns = ["metar_report", "cloud_cover"]
    df = df.drop(columns=[col for col in intermediate_columns if col in df.columns])

    df = df.sort_values("datetime").reset_index(drop=True)

    print(f"Final dataset: {len(df):,} records")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")

    return df


def extract_weather_type_from_metar(df: pd.DataFrame) -> pd.DataFrame:
    def parse_weather_types(metar):
        if pd.isna(metar):
            return set()

        weather_phenomena = {
            "RA": "rain",
            "SN": "snow",
            "DZ": "drizzle",
            "SG": "snow_grains",
            "IC": "ice_crystals",
            "PL": "ice_pellets",
            "GR": "hail",
            "GS": "small_hail",
            "UP": "unknown_precipitation",
            "BR": "mist",
            "FG": "fog",
            "FU": "smoke",
            "VA": "volcanic_ash",
            "DU": "dust",
            "SA": "sand",
            "HZ": "haze",
            "PY": "spray",
            "PO": "dust_whirls",
            "SQ": "squalls",
            "FC": "funnel_cloud",
            "SS": "sandstorm",
            "DS": "duststorm",
            "TS": "thunderstorm",
            "SH": "showers",
            "FZ": "freezing",
            "MI": "shallow",
            "PR": "partial",
            "BC": "patches",
            "DR": "drifting",
            "BL": "blowing",
        }

        intensity_map = {"-": "light", "+": "heavy", "VC": "vicinity"}
        found_weather = set()

        pattern = r"(-|\+|VC)?(MI|PR|BC|DR|BL|SH|TS|FZ)?([A-Z]{2})"
        matches = re.findall(pattern, metar)

        for intensity, descriptor, phenomenon in matches:
            if phenomenon in weather_phenomena:
                weather_name = weather_phenomena[phenomenon]

                if intensity and intensity in intensity_map:
                    weather_name = f"{intensity_map[intensity]}_{weather_name}"

                if descriptor and descriptor in weather_phenomena:
                    descriptor_name = weather_phenomena[descriptor]
                    weather_name = f"{descriptor_name}_{weather_name}"

                found_weather.add(weather_name)

        return found_weather

    df["weather_types"] = df["metar_report"].apply(parse_weather_types)

    all_weather_types = set()
    for types in df["weather_types"]:
        all_weather_types.update(types)

    for weather_type in sorted(all_weather_types):
        df[f"weather_{weather_type}"] = df["weather_types"].apply(
            lambda x: weather_type in x
        )

    df = df.drop(columns=["weather_types"])
    return df


def add_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    df["temperature_celsius"] = df["temperature"]
    df["freezing_conditions"] = df["temperature"] <= 0

    df["wind_speed_category"] = pd.cut(
        df["wind_speed"],
        bins=[0, 10, 20, 30, float("inf")],
        labels=["calm", "light", "moderate", "strong"],
        include_lowest=True,
    )

    def calculate_crosswind(wind_dir, wind_speed, runway_heading=40):
        if pd.isna(wind_dir) or pd.isna(wind_speed):
            return np.nan
        wind_angle = abs(wind_dir - runway_heading)
        if wind_angle > 180:
            wind_angle = 360 - wind_angle
        return wind_speed * np.sin(np.radians(wind_angle))

    df["crosswind_component"] = df.apply(
        lambda row: calculate_crosswind(row["wind_direction"], row["wind_speed"]),
        axis=1,
    )

    df["visibility_category"] = pd.cut(
        df["visibility"],
        bins=[0, 1, 3, 5, 10, float("inf")],
        labels=["very_poor", "poor", "marginal", "good", "excellent"],
        include_lowest=True,
    )

    def calculate_cloud_score(row):
        coverage_map = {"CLR": 0, "SKC": 0, "FEW": 2, "SCT": 4, "BKN": 6, "OVC": 8}
        layer = row["cloud_cover"]
        return coverage_map.get(layer, 0) if pd.notna(layer) else 0

    df["cloud_coverage_score"] = df.apply(calculate_cloud_score, axis=1)

    def get_ceiling(row):
        coverage = row["cloud_cover"]
        height = row["cloud_height"]
        if coverage in ["BKN", "OVC"] and pd.notna(height):
            return height
        return 99999

    df["ceiling_height"] = df.apply(get_ceiling, axis=1)

    df["ifr_conditions"] = (df["ceiling_height"] < 1000) | (df["visibility"] < 3)
    df["mvfr_conditions"] = (
        (df["ceiling_height"] >= 1000) & (df["ceiling_height"] < 3000)
    ) | ((df["visibility"] >= 3) & (df["visibility"] < 5))

    df["has_precipitation"] = df["precipitation"] > 0
    df["precipitation_category"] = pd.cut(
        df["precipitation"],
        bins=[0, 0.01, 0.1, 0.5, float("inf")],
        labels=["none", "trace", "light", "heavy"],
        include_lowest=True,
    )

    df["low_pressure"] = df["pressure"] < 1013.25
    df["pressure_category"] = pd.cut(
        df["pressure"],
        bins=[0, 1000, 1013.25, 1030, float("inf")],
        labels=["very_low", "low", "normal", "high"],
        include_lowest=True,
    )

    return df


def analyze_weather_data(df: pd.DataFrame):
    print("\n=== Weather Data Analysis ===")
    print(f"Total records: {len(df):,}")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")

    print("\n--- Missing Data Summary ---")
    missing_summary = df.isnull().sum()
    missing_summary = missing_summary[missing_summary > 0].sort_values(ascending=False)
    for col, count in missing_summary.items():
        percentage = (count / len(df)) * 100
        print(f"{col}: {count:,} ({percentage:.2f}%)")

    print("\n--- Key Weather Conditions ---")

    if "ifr_conditions" in df.columns:
        ifr_count = df["ifr_conditions"].sum()
        ifr_percentage = (ifr_count / len(df)) * 100
        print(f"IFR conditions: {ifr_count:,} records ({ifr_percentage:.2f}%)")

    if "mvfr_conditions" in df.columns:
        mvfr_count = df["mvfr_conditions"].sum()
        mvfr_percentage = (mvfr_count / len(df)) * 100
        print(f"MVFR conditions: {mvfr_count:,} records ({mvfr_percentage:.2f}%)")

    if "has_precipitation" in df.columns:
        precip_count = df["has_precipitation"].sum()
        precip_percentage = (precip_count / len(df)) * 100
        print(
            f"Records with precipitation: {precip_count:,} ({precip_percentage:.2f}%)"
        )

    weather_columns = [col for col in df.columns if col.startswith("weather_")]
    if weather_columns:
        print(f"\n--- Weather Types Found ({len(weather_columns)} types) ---")
        weather_counts = []
        for col in weather_columns:
            count = df[col].sum()
            if count > 0:
                weather_counts.append((col.replace("weather_", ""), count))

        weather_counts.sort(key=lambda x: x[1], reverse=True)
        for weather_type, count in weather_counts[:10]:
            percentage = (count / len(df)) * 100
            print(f"{weather_type}: {count:,} ({percentage:.2f}%)")

    print(f"\nFinal dataset shape: {df.shape}")
    print(f"Total features: {len(df.columns)}")
