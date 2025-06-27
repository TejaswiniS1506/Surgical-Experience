import pandas as pd
import os

# Load cleaned RUCA file
ruca_path = "tasks/medicare_data/output/ruca_cleaned.csv"
df_ruca = pd.read_csv(ruca_path, dtype=str)

# Convert ZIP code to 5-digit format
df_ruca["ZIP_CODE"] = df_ruca["ZIP_CODE"].str.zfill(5)

# Years we have data for
years = [2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023]

for year in years:
    print(f"Processing {year}...")
    input_path = f"tasks/medicare_data/output/tagged_procedures_{year}.csv"
    output_path = f"tasks/medicare_data/output/tagged_procedures_ruca_{year}.csv"

    if not os.path.exists(input_path):
        print(f"Skipping {year}: file not found.")
        continue

    df = pd.read_csv(input_path, dtype=str)
    df["Rndrng_Prvdr_Zip5"] = df["Rndrng_Prvdr_Zip5"].str.zfill(5)

    # Merge RUCA codes by zip code
    df_merged = df.merge(df_ruca, how="left", left_on="Rndrng_Prvdr_Zip5", right_on="ZIP_CODE")

    # Save merged file
    df_merged.to_csv(output_path, index=False)
    print(f"Saved RUCA-merged file for {year} to: {output_path}")
