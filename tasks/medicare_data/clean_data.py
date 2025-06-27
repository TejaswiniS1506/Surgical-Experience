# tasks/medicare_data/clean_data.py

import pandas as pd
import zipfile
import os

# Paths
MEDICARE_ZIP = "download_data/medicare_data.zip"
EXTRACT_FOLDER = "download_data/medicare/"
BETOS_CSV = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"
OUTPUT_FILE = "tasks/medicare_data/output/cleaned_medicare.csv"

def unzip_all():
    print("Unzipping Medicare data...")
    with zipfile.ZipFile(MEDICARE_ZIP, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)
    print("Unzipped outer zip.")

    # Find inner zip (e.g., CPS MDCR PHYSSUPP 2021.zip)
    for root, dirs, files in os.walk(EXTRACT_FOLDER):
        for file in files:
            if file.endswith(".zip") and "PHYSSUPP" in file:
                inner_zip_path = os.path.join(root, file)
                print(f"Unzipping inner zip: {inner_zip_path}")
                with zipfile.ZipFile(inner_zip_path, 'r') as inner_zip:
                    inner_zip.extractall(root)
                return root  # Excel will be inside here
    raise FileNotFoundError("Inner ZIP file not found.")

def get_major_procedures():
    print("Reading BETOS mapping...")
    df_betos = pd.read_csv(BETOS_CSV)
    major_set = set(df_betos[df_betos["RBCS_Major_Ind"] == "M"]["HCPCS_CD"])
    print(f"{len(major_set)} major procedure codes found.")
    return major_set

def clean_medicare():
    data_dir = unzip_all()
    excel_path = None

    for file in os.listdir(data_dir):
        if file.endswith(".xlsx") and "PHYSSUPP" in file:
            excel_path = os.path.join(data_dir, file)
            break

    if not excel_path:
        raise FileNotFoundError("No Medicare Excel file found after unzip.")

    print(f"Reading Excel file: {excel_path}")
    df = pd.read_excel(excel_path, dtype=str)

    major_procs = get_major_procedures()

    if "HCPCS" not in df.columns:
        raise KeyError("Column 'HCPCS' not found in Medicare Excel file.")

    print("Filtering rows by major procedures...")
    filtered = df[df["HCPCS"].isin(major_procs)]

    print(f"Saving {len(filtered)} rows to {OUTPUT_FILE}...")
    filtered.to_csv(OUTPUT_FILE, index=False)
    print("✅ Done!")

if __name__ == "__main__":
    clean_medicare()
