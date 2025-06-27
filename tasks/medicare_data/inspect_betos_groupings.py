import pandas as pd

betos_path = "download_data/Restructured BETOS Classification System/2024/2024 RBCS Taxonomy_CSV.csv"

df_betos = pd.read_csv(betos_path)

# Print all columns again just for clarity
print("\nBETOS file columns:")
for col in df_betos.columns:
    print(f" - {col}")

# Explore major procedure indicator and possible grouping columns
grouping_summary = {
    "RBCS_Major_Ind": df_betos["RBCS_Major_Ind"].dropna().unique().tolist(),
    "RBCS_Family_Desc": df_betos["RBCS_Family_Desc"].dropna().unique().tolist(),
    "RBCS_SubCat_Desc": df_betos["RBCS_SubCat_Desc"].dropna().unique().tolist()
}

print("\n\nSample values for potential grouping columns:")
for k, v in grouping_summary.items():
    print(f"\n{k} ({len(v)} unique values):")
    print(v[:10])  # Show just first 10 group values
