import pandas as pd
import json
from datetime import datetime
from pathlib import Path

from extractor.youtube_client import YouTubeClient

videos_df = pd.read_csv(
    "data/processed/trending_videos.csv"
)

channel_ids = (
    videos_df["channel_id"]
    .dropna()
    .unique()
    .tolist()
)

print(f"Unique channels: {len(channel_ids)}")

client = YouTubeClient()

all_channels = []


def keep_latest(pattern):

    files = sorted(
        Path("data/raw").glob(pattern),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    for file in files[1:]:
        file.unlink()
        print(f"Deleted old file: {file}")


for i in range(0, len(channel_ids), 50):

    batch = channel_ids[i:i + 50]

    print(
        f"Fetching batch "
        f"{i // 50 + 1} "
        f"({len(batch)} channels)"
    )

    data = client.get_channels(batch)

    all_channels.extend(
        data.get("items", [])
    )

print(
    f"\nTotal channels fetched: "
    f"{len(all_channels)}"
)

output_data = {
    "items": all_channels
}

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

filename = (
    f"data/raw/channels_{timestamp}.json"
)

with open(
    filename,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output_data,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved: {filename}")

keep_latest("channels_*.json")