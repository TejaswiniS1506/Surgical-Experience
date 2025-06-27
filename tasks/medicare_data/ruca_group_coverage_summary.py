import pandas as pd
import os

# Define groups
def ruca_group(ruca):
    if ruca in [1, 2]:
        return "Group 1-2"
    elif ruca in [3, 4]:
        return "Group 3-4"
    elif ruca in [5, 6]:
        return "Group 5-6"
    elif ruca in [7, 8]:
        return "Group 7-8"
    elif ruca in [9, 10]:
        return "Group 9-10"
    return None

years = [2013, 2023]

for year in years:
    print(f"\nAnalyzing {year}...")
    path = f"tasks/medicare_data/output/experience_by_ruca_{year}.csv"
    df = pd.read_csv(path)

    # Clean and group
    df["RUCA1"] = pd.to_numeric(df["RUCA1"], errors="coerce")
    df["RUCA_Group"] = df["RUCA1"].apply(ruca_group)
    df = df.dropna(subset=["RUCA_Group"])

    # Count how many groups each procedure family appears in
    family_group_counts = (
        df.groupby("RBCS_Family_Desc")["RUCA_Group"]
        .nunique()
        .reset_index(name="num_ruca_groups")
    )

    # Save which families occur in all 5 groups
    full_coverage = family_group_counts[family_group_counts["num_ruca_groups"] == 5]
    full_coverage_list = full_coverage["RBCS_Family_Desc"].tolist()

    # Output
    with open(f"tasks/medicare_data/output/procedure_ruca_coverage_{year}.txt", "w") as f:
        f.write(f"Year: {year}\n")
        f.write(f"Procedure families that appear in all 5 RUCA groups: {len(full_coverage_list)}\n\n")
        f.write("\n".join(full_coverage_list))

    print(f"Saved coverage summary for {year}.")
