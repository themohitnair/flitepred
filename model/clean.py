import os
import pandas as pd

# File paths
processed_data_path = "dataset/processed"
input_file = os.path.join(processed_data_path, "jfk_combined_2024.csv")
output_file = os.path.join(processed_data_path, "jfk_cleaned_2024.csv")

# Load the data
df = pd.read_csv(input_file)

# Extract just the hour from DEP_TIME and store it in DEP_HOUR
df["DEP_HOUR"] = (df["DEP_TIME"] // 100).astype(int)

# Extract minutes and store it in DEP_MINUTE
df["DEP_MINUTE"] = (df["DEP_TIME"] % 100).astype(int)

# Remove unwanted columns (ORIGIN_AIRPORT_ID, DEP_DATE)
df_cleaned = df.drop(columns=["ORIGIN_AIRPORT_ID", "DEP_DATE"])

# Save the cleaned data to the output file
df_cleaned.to_csv(output_file, index=False)
print(f"Cleaned file saved to {output_file}")
