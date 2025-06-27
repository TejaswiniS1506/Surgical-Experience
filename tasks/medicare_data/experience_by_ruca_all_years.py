import pandas as pd
import os

years = [2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023]

for year in years:
    print(f"Processing {year}...")
    input_path = f"tasks/medicare_data/output/tagged_procedures_ruca_{year}.csv"
    output_path = f"tasks/medicare_data/output/experience_by_ruca_{year}.csv"

    if not os.path.exists(input_path):
        print(f"Skipping {year}: File not found.")
        continue

    df = pd.read_csv(input_path, dtype=str)

    # Keep only major procedures
    df = df[df["RBCS_Major_Ind"] == "M"].copy()

    # Convert necessary columns
    df["Tot_Srvcs"] = pd.to_numeric(df["Tot_Srvcs"], errors="coerce")
    df["RUCA1"] = pd.to_numeric(df["RUCA1"], errors="coerce")

    # Group by procedure family and RUCA level
    agg = (
        df.groupby(["RBCS_Family_Desc", "RUCA1"])
        .agg(
            total_procedures=("Tot_Srvcs", "sum"),
            unique_doctors=("Rndrng_NPI", "nunique")
        )
        .reset_index()
    )

    # Save output
    agg.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")
