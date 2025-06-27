import pandas as pd

file_path = "download_data/medicare_data_2013/Medicare Physician & Other Practitioners - by Provider and Service/2013/MUP_PHY_R25_P04_V10_D13_Prov_Svc.csv"

try:
    df = pd.read_csv(file_path, nrows=5)  # Only read the first few rows
    print("✅ Successfully loaded file.")
    print("📋 Column names:")
    print(df.columns.tolist())
except Exception as e:
    print("❌ Error while reading file:")
    print(e)
