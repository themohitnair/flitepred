import numpy as np
import pandas as pd


def impute_and_clean_dataset(file_path):
    """
    Impute critical weather columns and drop rows with remaining missing values
    """
    print("Loading dataset...")
    df = pd.read_csv(file_path)

    print(f"Original dataset shape: {df.shape}")
    print(f"Original missing values: {df.isnull().sum().sum()}")

    # 1. Impute cloud_height (fixed pandas warning)
    cloud_missing_before = df["cloud_height"].isnull().sum()
    if cloud_missing_before > 0:
        actual_clouds = df[
            (df["cloud_height"].notna()) & (df["cloud_height"] != 99999)
        ]["cloud_height"]
        if len(actual_clouds) > 0:
            cloud_median = actual_clouds.median()
        else:
            cloud_median = 5000.0

        df["cloud_height"] = df["cloud_height"].fillna(cloud_median)  # Fixed syntax
        print(
            f"✅ Imputed {cloud_missing_before} cloud_height values with median: {cloud_median}"
        )

    # 2. Impute wind_direction (fixed pandas warning)
    wind_missing_before = df["wind_direction"].isnull().sum()
    if wind_missing_before > 0:
        wind_median = df["wind_direction"].median()
        df["wind_direction"] = df["wind_direction"].fillna(wind_median)  # Fixed syntax
        print(
            f"✅ Imputed {wind_missing_before} wind_direction values with median: {wind_median}"
        )

    # 3. Recalculate crosswind_component
    def calculate_crosswind(wind_dir, wind_speed, runway_heading=40):
        if pd.isna(wind_dir) or pd.isna(wind_speed):
            return np.nan
        wind_angle = abs(wind_dir - runway_heading)
        if wind_angle > 180:
            wind_angle = 360 - wind_angle
        return wind_speed * np.sin(np.radians(wind_angle))

    crosswind_missing_before = df["crosswind_component"].isnull().sum()

    df["crosswind_component"] = df.apply(
        lambda row: calculate_crosswind(row["wind_direction"], row["wind_speed"]),
        axis=1,
    )

    crosswind_missing_after = df["crosswind_component"].isnull().sum()
    crosswind_imputed = crosswind_missing_before - crosswind_missing_after
    print(f"✅ Recalculated crosswind_component, imputed {crosswind_imputed} values")

    # 4. Drop rows with remaining missing values
    rows_before = len(df)
    missing_before_drop = df.isnull().sum().sum()

    df = df.dropna()

    rows_after = len(df)
    rows_dropped = rows_before - rows_after
    missing_after_drop = df.isnull().sum().sum()

    print("\n=== Cleanup Summary ===")
    print(f"Rows dropped: {rows_dropped:,} ({(rows_dropped / rows_before) * 100:.2f}%)")
    print(f"Missing values before drop: {missing_before_drop:,}")
    print(f"Missing values after drop: {missing_after_drop:,}")

    print("\n=== Final Dataset ===")
    print(f"Final dataset shape: {df.shape}")
    print("Data completeness: 100%")
    print("✅ Dataset is now completely clean with no missing values!")

    # Save cleaned dataset
    output_path = file_path.replace(".csv", "_clean.csv")
    df.to_csv(output_path, index=False)
    print(f"\n💾 Clean dataset saved to: {output_path}")

    return df
