import pandas as pd

years = [2013, 2023]
thresholds = [2, 3, 4]

for year in years:
    print(f"\nProcessing {year}...")
    path = f"tasks/medicare_data/output/experience_by_ruca_{year}.csv"
    df = pd.read_csv(path)
    df["RUCA1"] = pd.to_numeric(df["RUCA1"], errors="coerce")

    with open(f"tasks/medicare_data/output/procedure_urban_coverage_{year}.txt", "w") as f:
        f.write(f"Urban Coverage Summary for {year}\n")
        f.write("=" * 40 + "\n\n")

        for threshold in thresholds:
            filtered = df[df["RUCA1"] > threshold]
            unique_procedures = filtered["RBCS_Family_Desc"].nunique()
            f.write(f"RUCA1 > {threshold}: {unique_procedures} unique procedure families\n")

    print(f"Saved urbanicity breakdown for {year}.")
