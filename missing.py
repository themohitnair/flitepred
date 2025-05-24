from preprocessing.impute import impute_and_clean_dataset

file_path = "dataset/processed/jfk_optimized.csv"
clean_df = impute_and_clean_dataset(file_path)
