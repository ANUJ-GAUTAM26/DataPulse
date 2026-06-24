import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Find latest trending videos file only
raw_folder = Path("data/raw")

video_files = list(
    raw_folder.glob("trending_videos_*.json")
)

if not video_files:
    raise FileNotFoundError(
        "No trending_videos JSON files found in data/raw"
    )

latest_file = max(
    video_files,
    key=lambda x: x.stat().st_mtime
)

print(f"Reading file: {latest_file}")

# Load JSON
with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

# Extract fields
for item in data.get("items", []):

    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})

    rows.append({
    "video_id": item.get("id"),
    "title": snippet.get("title"),
    "channel_id": snippet.get("channelId"),
    "channel_title": snippet.get("channelTitle"),
    "published_at": snippet.get("publishedAt"),
    "category_id": snippet.get("categoryId"),
    "region_code": item.get("region_code"),
    "view_count": statistics.get("viewCount"),
    "like_count": statistics.get("likeCount"),
    "comment_count": statistics.get("commentCount"),
    "extraction_date": datetime.now().date()
})

print(f"Raw items: {len(rows)}")

# Create DataFrame
df = pd.DataFrame(rows)

# Data Cleaning
df["view_count"] = pd.to_numeric(
    df["view_count"],
    errors="coerce"
).fillna(0).astype("int64")

df["like_count"] = pd.to_numeric(
    df["like_count"],
    errors="coerce"
).fillna(0).astype("int64")

df["comment_count"] = pd.to_numeric(
    df["comment_count"],
    errors="coerce"
).fillna(0).astype("int64")

df["published_at"] = pd.to_datetime(
    df["published_at"],
    format="ISO8601",
    errors="coerce"
)

# Check duplicates
print(f"Rows before dedup: {len(df)}")

duplicate_count = df.duplicated(
    subset=["video_id"]
).sum()

print(f"Duplicate videos: {duplicate_count}")

# Remove duplicates
df = df.drop_duplicates(
    subset=["video_id"]
)

print(f"Rows after dedup: {len(df)}")

# Save CSV
output_file = "data/processed/trending_videos.csv"

df.to_csv(
    output_file,
    index=False
)

print(f"Saved processed data to: {output_file}")
print(f"Final Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")