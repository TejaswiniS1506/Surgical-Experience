import pandas as pd

# Load 2013 Medicare data
df_medicare = pd.read_csv("tasks/medicare_data/output/medicare_data_2013_cleaned.csv")


# Load BETOS taxonomy
betos_path = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"
df_betos = pd.read_csv(betos_path)

# Keep only major procedures (RBCS_Major_Ind == 'M')
df_betos_major = df_betos[df_betos["RBCS_Major_Ind"] == "M"][
    ["HCPCS_Cd", "RBCS_Family_Desc", "RBCS_Major_Ind"]
]

# Merge with Medicare data
df_tagged = df_medicare.merge(
    df_betos_major,
    how="inner",
    left_on="HCPCS_Cd",
    right_on="HCPCS_Cd"
)

# Save result
df_tagged.to_csv("tasks/medicare_data/output/tagged_procedures_2013.csv", index=False)
print("Tagged major procedures saved to: tasks/medicare_data/output/tagged_procedures_2013.csv")
