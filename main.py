from preprocessing.impute import impute_and_clean_dataset

file_path = "dataset/processed/jfk_optimized.csv"
clean_df = impute_and_clean_dataset(file_path)

print("\n=== Data Quality Check ===")
print("Label distribution:")
print(clean_df["label"].value_counts())
print("\nDataset ready for machine learning!")
