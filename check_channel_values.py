# check_channel_values.py

import pandas as pd

df = pd.read_csv("data/processed/channels.csv")

print(df.dtypes)

print("\nMAX VALUES\n")

for col in df.columns:
    if "count" in col.lower():
        print(f"{col}: {df[col].max()}")

print("\nTOP 5 ROWS\n")
print(df.head())