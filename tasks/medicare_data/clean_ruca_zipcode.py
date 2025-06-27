import pandas as pd

# Load raw RUCA data
ruca_path = "download_data/ruca/RUCA2010zipcode.csv"
df_ruca = pd.read_csv(ruca_path)

# Fix column names
df_ruca.rename(columns={"''ZIP_CODE''": "ZIP_CODE"}, inplace=True)

# Keep only necessary columns
columns_to_keep = ["ZIP_CODE", "RUCA1"]
df_cleaned = df_ruca[columns_to_keep].copy()

# Save cleaned file
output_path = "tasks/medicare_data/output/ruca_cleaned.csv"
df_cleaned.to_csv(output_path, index=False)

print(f"Cleaned RUCA data saved to: {output_path}")
