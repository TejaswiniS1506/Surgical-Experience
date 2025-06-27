import pandas as pd
import os

# BETOS classification CSV path
BETOS_PATH = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"
OUTPUT_CSV = "tasks/medicare_data/output/hcpcs_group_mapping.csv"

def explore_groupings():
    if not os.path.exists(BETOS_PATH):
        raise FileNotFoundError(f"BETOS file not found at: {BETOS_PATH}")

    print("Reading BETOS file...")
    df = pd.read_csv(BETOS_PATH, dtype=str)

    print("Filtering for major procedures...")
    major_df = df[df["RBCS_Major_Ind"] == "M"]

    print(f"Total HCPCS codes marked as major: {len(major_df)}")
    print("Number of unique groups:", major_df["RBCS_Grp_Desc"].nunique())
    print("\nSample of group distribution:")
    print(major_df["RBCS_Grp_Desc"].value_counts().head(10))

    print(f"\nSaving HCPCS-to-group mapping to: {OUTPUT_CSV}")
    major_df[["HCPCS_Cd", "RBCS_Grp_Desc"]].to_csv(OUTPUT_CSV, index=False)
    print("Done.")

if __name__ == "__main__":
    explore_groupings()
