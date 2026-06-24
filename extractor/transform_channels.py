import json
import pandas as pd
from pathlib import Path

# Find latest channels JSON file
raw_folder = Path("data/raw")

channel_files = list(
    raw_folder.glob("channels_*.json")
)

if not channel_files:
    raise FileNotFoundError(
        "No channels JSON files found in data/raw"
    )

latest_file = max(
    channel_files,
    key=lambda x: x.stat().st_mtime
)

print(f"Reading file: {latest_file}")

# Load JSON
with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# Extract channel information
for item in data.get("items", []):

    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})

    rows.append({
        "channel_id": item.get("id"),
        "channel_title": snippet.get("title"),
        "country": snippet.get("country"),
        "subscriber_count": statistics.get("subscriberCount"),
        "video_count": statistics.get("videoCount"),
        "total_view_count": statistics.get("viewCount")
    })

print(f"Raw channels: {len(rows)}")

# Create DataFrame
df = pd.DataFrame(rows)

# Data Cleaning
numeric_columns = [
    "subscriber_count",
    "video_count",
    "total_view_count"
]

for col in numeric_columns:

    df[col] = (
        pd.to_numeric(
            df[col],
            errors="coerce"
        )
        .fillna(0)
        .astype("int64")
    )

# Handle missing country values
df["country"] = df["country"].fillna("Unknown")

print(f"Rows before dedup: {len(df)}")

duplicate_count = df.duplicated(
    subset=["channel_id"]
).sum()

print(f"Duplicate channels: {duplicate_count}")

# Remove duplicates
df = df.drop_duplicates(
    subset=["channel_id"]
)

print(f"Rows after dedup: {len(df)}")

# Save CSV
output_file = "data/processed/channels.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"Saved processed data to: {output_file}")
print(f"Channels: {len(df)}")
print(f"Columns: {list(df.columns)}")

print("\nSample Data:")
print(df.head())