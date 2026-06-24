import json
from datetime import datetime
from pathlib import Path

from extractor.youtube_client import YouTubeClient

client = YouTubeClient()

REGIONS = [
    "IN",
    "US",
    "GB",
    "CA",
    "AU",
    "DE",
    "FR",
    "JP",
    "KR",
    "BR"
]


def keep_latest(pattern):

    files = sorted(
        Path("data/raw").glob(pattern),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    for file in files[1:]:
        file.unlink()
        print(f"Deleted old file: {file}")


all_items = []

print("Starting extraction...\n")

for region in REGIONS:

    print(f"Fetching region: {region}")

    data = client.get_trending_videos(
        region_code=region
    )

    videos = data.get("items", [])

    print(f"Fetched {len(videos)} videos")

    for video in videos:
        video["region_code"] = region

    all_items.extend(videos)

print("\nExtraction completed!")
print(f"Total raw records: {len(all_items)}")

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

filename = (
    f"data/raw/trending_videos_{timestamp}.json"
)

with open(
    filename,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        {"items": all_items},
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved to: {filename}")

keep_latest("trending_videos_*.json")