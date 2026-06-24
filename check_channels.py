import pandas as pd

print("Loading files...\n")

videos = pd.read_csv("data/processed/trending_videos.csv")
channels = pd.read_csv("data/processed/channels.csv")

video_channels = set(videos["channel_id"].unique())
channel_ids = set(channels["channel_id"].unique())

missing = video_channels - channel_ids

print(f"Total video rows: {len(videos)}")
print(f"Unique video channels: {len(video_channels)}")
print(f"Channels CSV rows: {len(channels)}")
print(f"Unique channels in CSV: {len(channel_ids)}")
print(f"Missing channels: {len(missing)}")

if missing:
    print("\nMissing Channel IDs:")
    print("-" * 50)

    for channel_id in sorted(missing):
        print(channel_id)
else:
    print("\nNo missing channels found!")