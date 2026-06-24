import pandas as pd

from loader.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# =========================
# LOAD CHANNELS
# =========================

channels_df = pd.read_csv(
    "data/processed/channels.csv"
)

channels_df["subscriber_count"] = (
    pd.to_numeric(
        channels_df["subscriber_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

channels_df["video_count"] = (
    pd.to_numeric(
        channels_df["video_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

channels_df["total_view_count"] = (
    pd.to_numeric(
        channels_df["total_view_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

channels_df["country"] = (
    channels_df["country"]
    .fillna("Unknown")
)

for _, row in channels_df.iterrows():

    cursor.execute("""
        INSERT INTO dim_channel (
            channel_id,
            channel_title,
            country,
            subscriber_count,
            video_count,
            total_view_count
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (channel_id) DO NOTHING
    """,
    (
        row["channel_id"],
        row["channel_title"],
        row["country"],
        int(row["subscriber_count"]),
        int(row["video_count"]),
        int(row["total_view_count"])
    ))

conn.commit()

print("Channels loaded!")

# =========================
# LOAD VIDEOS
# =========================

videos_df = pd.read_csv(
    "data/processed/trending_videos.csv"
)

videos_df["view_count"] = (
    pd.to_numeric(
        videos_df["view_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

videos_df["like_count"] = (
    pd.to_numeric(
        videos_df["like_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

videos_df["comment_count"] = (
    pd.to_numeric(
        videos_df["comment_count"],
        errors="coerce"
    )
    .fillna(0)
    .astype("int64")
)

for _, row in videos_df.iterrows():

    try:

        cursor.execute("""
            INSERT INTO fact_video_metrics (
                video_id,
                title,
                channel_id,
                category_id,
                published_at,
                view_count,
                like_count,
                comment_count,
                extraction_date
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (video_id) DO NOTHING
        """,
        (
            row["video_id"],
            row["title"],
            row["channel_id"],
            str(row["category_id"]),
            row["published_at"],
            int(row["view_count"]),
            int(row["like_count"]),
            int(row["comment_count"]),
            row["extraction_date"]
        ))

    except Exception as e:

        print("\nFAILED VIDEO ROW:")
        print(row)
        print(f"\nERROR: {e}")

        raise

conn.commit()

print("Videos loaded!")

cursor.close()
conn.close()

print("Data loading completed successfully!")