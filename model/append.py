import os
import pandas as pd

raw_data_path = "dataset/raw"
processed_data_path = "dataset/processed"
output_file = "dataset/processed/jfk_ontime_2024.csv"

os.makedirs(processed_data_path, exist_ok=True)

dfs = []

for month_dir in os.listdir(raw_data_path):
    month_path = os.path.join(raw_data_path, month_dir)
    if os.path.isdir(month_path):
        csv_path = os.path.join(month_path, "T_ONTIME_REPORTING.csv")
        if os.path.exists(csv_path):
            print(f"Reading {csv_path}")
            df = pd.read_csv(csv_path)

            df_filtered = df[df["ORIGIN_AIRPORT_ID"] == 12478]
            dfs.append(df_filtered)

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df.to_csv(output_file, index=False)
    print(f"Combined filtered file saved to {output_file}")
else:
    print("No CSV files found to concatenate or no data matched the filter.")
