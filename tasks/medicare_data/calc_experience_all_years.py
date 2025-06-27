import pandas as pd
import os

# Years you have data for
years = [2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023]

for year in years:
    try:
        print(f"Processing {year}...")

        # Load the tagged procedures
        df = pd.read_csv(f"tasks/medicare_data/output/tagged_procedures_{year}.csv", low_memory=False)

        # Filter to major procedures only
        df_major = df[df["RBCS_Major_Ind"] == "M"]

        # Group by doctor and family
        doctor_experience = (
            df_major.groupby(["Rndrng_NPI", "RBCS_Family_Desc"])["Tot_Srvcs"]
            .sum()
            .reset_index()
            .rename(columns={"Tot_Srvcs": "Total_Procedures"})
        )
        doctor_output_path = f"tasks/medicare_data/output/experience_by_doctor_{year}.csv"
        doctor_experience.to_csv(doctor_output_path, index=False)

        # Group by procedure family across all doctors
        family_experience = (
            df_major.groupby("RBCS_Family_Desc")["Tot_Srvcs"]
            .sum()
            .reset_index()
            .rename(columns={"Tot_Srvcs": "Total_Procedures_All_Doctors"})
        )
        family_output_path = f"tasks/medicare_data/output/experience_by_family_{year}.csv"
        family_experience.to_csv(family_output_path, index=False)

        print(f"Saved doctor experience to: {doctor_output_path}")
        print(f"Saved family totals to: {family_output_path}")

    except FileNotFoundError:
        print(f"Skipping {year}: tagged file not found.")
