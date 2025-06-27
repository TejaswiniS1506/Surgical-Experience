import pandas as pd
import os

# Define paths
betos_path = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"
input_folder = "tasks/medicare_data/output/"
output_folder = "tasks/medicare_data/output/"

# Load BETOS taxonomy and filter major procedures
df_betos = pd.read_csv(betos_path)
df_betos_major = df_betos[df_betos["RBCS_Major_Ind"] == "M"][
    ["HCPCS_Cd", "RBCS_Family_Desc", "RBCS_Major_Ind"]
]

# Loop through 2013–2023
for year in range(2013, 2024):
    input_file = f"{input_folder}medicare_data_{year}_cleaned.csv"
    output_file = f"{output_folder}tagged_procedures_{year}.csv"

    if not os.path.exists(input_file):
        print(f"Skipping {year}: File not found.")
        continue

    print(f"Processing {year}...")
    df_medicare = pd.read_csv(input_file, low_memory=False)
    df_tagged = df_medicare.merge(
        df_betos_major,
        how="inner",
        on="HCPCS_Cd"
    )
    df_tagged.to_csv(output_file, index=False)
    print(f"Saved tagged procedures for {year} to: {output_file}")
