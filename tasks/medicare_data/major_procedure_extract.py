import os
import sys
import pandas as pd

# Step 0: Read year from command-line
year = sys.argv[1]

# Step 1: Build correct file paths
year_dir = os.path.join(
    f"download_data/medicare_data_{year}",
    "Medicare Physician & Other Practitioners - by Provider and Service",
    year
)

# BETOS file path (assumed static)
betos_path = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"

# Output file path
output_path = f"tasks/medicare_data/output/medicare_data_{year}_cleaned.csv"

# Step 2: Find .csv or .xlsx file in the year folder
data_files = [f for f in os.listdir(year_dir) if f.endswith(".xlsx") or f.endswith(".csv")]
data_file = None
for f in data_files:
    if "Prov" in f or "Service" in f:
        data_file = f
        break
if not data_file:
    raise FileNotFoundError(f"No valid Medicare provider data file found for year {year}.")

data_path = os.path.join(year_dir, data_file)
print(" Reading Medicare data from:", data_path)

# Step 3: Load BETOS codes and extract "Major Procedures"
print(" Reading BETOS classification file...")
betos_df = pd.read_csv(betos_path, dtype=str)
major_codes = set(betos_df[betos_df["RBCS_Major_Ind"] == "M"]["HCPCS_Cd"].astype(str))
print(f" Found {len(major_codes)} major procedure codes.")

# Step 4: Read the Medicare data in chunks and filter by major codes
print(" Filtering Medicare data in chunks...")
chunksize = 10000
reader = pd.read_excel(data_path, dtype=str, chunksize=chunksize) if data_path.endswith(".xlsx") else pd.read_csv(data_path, dtype=str, chunksize=chunksize)

for i, chunk in enumerate(reader):
    if "HCPCS_Cd" not in chunk.columns:
        raise KeyError("Column 'HCPCS_Cd' not found in the data file.")

    filtered = chunk[chunk["HCPCS_Cd"].astype(str).isin(major_codes)]
    mode = 'w' if i == 0 else 'a'
    header = i == 0
    filtered.to_csv(output_path, mode=mode, header=header, index=False)
    print(f" Chunk {i+1} processed and written...")

print(f"\n Done! Extract saved to: {output_path}")
