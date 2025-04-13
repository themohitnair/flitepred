import pandas as pd

input_file = "dataset/processed/jfk_cleaned_2024.csv"
output_file = "dataset/processed/jfk_top5_dests_top3_carriers.csv"

df = pd.read_csv(input_file)

top_5_destinations = df["DEST_AIRPORT_ID"].value_counts().head(5).index
df_top5_dest = df[df["DEST_AIRPORT_ID"].isin(top_5_destinations)]

top_3_carriers = df_top5_dest["OP_UNIQUE_CARRIER"].value_counts().head(3).index
df_top5_dests_top3_carriers = df_top5_dest[
    df_top5_dest["OP_UNIQUE_CARRIER"].isin(top_3_carriers)
]

df_top5_dests_top3_carriers.to_csv(output_file, index=False)

print(f"Top 5 DEST_AIRPORT_IDs: {top_5_destinations}")
print(f"Top 3 Carriers: {top_3_carriers}")
print("Filtered data saved to:", output_file)
