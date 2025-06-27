import pandas as pd
import matplotlib.pyplot as plt
import os

def compute_doctor_weighted_avg(df):
    df = df.copy()
    df["doctor_weighted_avg"] = df["total_procedures"] / df["unique_doctors"]
    return df[["RBCS_Family_Desc", "RUCA1", "doctor_weighted_avg"]]

# Load files
df_2013 = pd.read_csv("tasks/medicare_data/output/experience_by_ruca_2013.csv")
df_2023 = pd.read_csv("tasks/medicare_data/output/experience_by_ruca_2023.csv")

avg_2013 = compute_doctor_weighted_avg(df_2013)
avg_2023 = compute_doctor_weighted_avg(df_2023)

# Combine both years for plotting
combined = avg_2013.merge(
    avg_2023, on=["RBCS_Family_Desc", "RUCA1"], suffixes=("_2013", "_2023")
)

# Make output folder if needed
os.makedirs("tasks/medicare_data/output/plots", exist_ok=True)

# Plot each procedure group
for group in combined["RBCS_Family_Desc"].unique():
    subset = combined[combined["RBCS_Family_Desc"] == group]

    plt.figure()
    plt.plot(subset["RUCA1"], subset["doctor_weighted_avg_2013"], label="2013", marker='o')
    plt.plot(subset["RUCA1"], subset["doctor_weighted_avg_2023"], label="2023", marker='o')
    plt.xlabel("RUCA1 Level")
    plt.ylabel("Doctor-Weighted Average Experience")
    plt.title(f"{group} – Doctor-Weighted Avg by RUCA")
    plt.legend()
    plt.grid(True)

    filename = f"tasks/medicare_data/output/plots/doctor_weighted_avg_{group.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()

print("All doctor-weighted average plots saved!")
