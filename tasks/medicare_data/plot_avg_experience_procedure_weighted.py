import pandas as pd
import matplotlib.pyplot as plt
import os

input_dir = "tasks/medicare_data/output"
output_dir = os.path.join(input_dir, "plots_procedure_weighted")
os.makedirs(output_dir, exist_ok=True)

def load_and_prepare(year):
    df = pd.read_csv(f"{input_dir}/experience_by_ruca_{year}.csv")
    return df

def compute_avg(df):
    # Drop rows with missing or zero procedures to avoid division by zero
    df = df[df["total_procedures"] != 0]

    grouped = df.groupby(["RBCS_Family_Desc", "RUCA1"]).agg(
        total_experience=("total_procedures", "sum"),
        count=("total_procedures", "count")
    ).reset_index()

    grouped["avg_experience"] = grouped["total_experience"] / grouped["count"]
    return grouped[["RBCS_Family_Desc", "RUCA1", "avg_experience"]]


def plot_avg(df_2013, df_2023):
    procedures = set(df_2013["RBCS_Family_Desc"]).union(set(df_2023["RBCS_Family_Desc"]))

    for proc in procedures:
        plt.figure(figsize=(8, 5))
        sub_2013 = df_2013[df_2013["RBCS_Family_Desc"] == proc]
        sub_2023 = df_2023[df_2023["RBCS_Family_Desc"] == proc]

        plt.plot(sub_2013["RUCA1"], sub_2013["avg_experience"], label="2013", marker="o")
        plt.plot(sub_2023["RUCA1"], sub_2023["avg_experience"], label="2023", marker="x")

        plt.xlabel("RUCA Level")
        plt.ylabel("Avg Experience per Procedure")
        plt.title(f"{proc} – Procedure-Weighted")
        plt.legend()
        plt.tight_layout()

        # Clean file name
        fname = proc.replace("/", "-").replace(" ", "_") + "_procedure_weighted.png"
        plt.savefig(os.path.join(output_dir, fname))
        plt.close()

# Run
df_2013 = compute_avg(load_and_prepare(2013))
df_2023 = compute_avg(load_and_prepare(2023))
plot_avg(df_2013, df_2023)

print("All procedure-weighted average plots saved!")
