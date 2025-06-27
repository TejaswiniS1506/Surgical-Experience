import pandas as pd

df = pd.read_csv("tasks/medicare_data/output/tagged_procedures_2013.csv")
print("Columns:", df.columns.tolist())
