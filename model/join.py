import os
import pandas as pd

raw_data_path = "dataset/raw"
processed_data_path = "dataset/processed"
output_file = "dataset/processed/jfk_combined_2024.csv"

ontime_data_path = os.path.join(processed_data_path, "jfk_ontime_2024.csv")
ontime_df = pd.read_csv(ontime_data_path)

weather_data_path = os.path.join(raw_data_path, "jfk_weather_2024.csv")
weather_df = pd.read_csv(weather_data_path)

weather_df["time"] = pd.to_datetime(weather_df["time"])

ontime_df["DEP_TIME"] = pd.to_numeric(ontime_df["DEP_TIME"], errors="coerce")
ontime_df = ontime_df.dropna(subset=["DEP_TIME"])

ontime_df["DEP_TIME"] = ontime_df["DEP_TIME"].apply(lambda x: 0 if x == 2400 else x)

ontime_df["DEP_HOUR"] = (ontime_df["DEP_TIME"] // 100).astype(int)
ontime_df["DEP_MINUTE"] = (ontime_df["DEP_TIME"] % 100).astype(int)

ontime_df["DEP_DATE"] = pd.to_datetime(
    ontime_df["MONTH"].astype(str)
    + "-"
    + ontime_df["DAY_OF_MONTH"].astype(str)
    + "-2024 "
    + ontime_df["DEP_HOUR"].astype(str)
    + ":"
    + ontime_df["DEP_MINUTE"].astype(str),
    format="%m-%d-%Y %H:%M",
)

ontime_df["DEP_HOUR"] = ontime_df["DEP_DATE"].dt.floor("H")

ontime_df = ontime_df.dropna()

merged_df = pd.merge(
    ontime_df, weather_df, left_on="DEP_HOUR", right_on="time", how="left"
)

merged_df.drop(columns=["time"], inplace=True)

merged_df.to_csv(output_file, index=False)
print(f"Combined file saved to {output_file}")
