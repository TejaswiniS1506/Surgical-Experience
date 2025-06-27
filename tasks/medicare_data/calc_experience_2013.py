import pandas as pd

# Load the tagged 2013 data
df = pd.read_csv("tasks/medicare_data/output/tagged_procedures_2013.csv")

# Filter to major procedures only
df_major = df[df["RBCS_Major_Ind"] == "M"]

# Group by doctor and procedure group
experience = (
    df_major.groupby(["Rndrng_NPI", "RBCS_Family_Desc"])["Tot_Srvcs"]
    .sum()
    .reset_index()
    .rename(columns={"Tot_Srvcs": "Total_Procedures"})
)

# Save to CSV
output_path = "tasks/medicare_data/output/experience_by_doctor_2013.csv"
experience.to_csv(output_path, index=False)

print(f"Saved experience data to: {output_path}")
