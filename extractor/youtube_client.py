import requests
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

BASE_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeClient:

    def get_trending_videos(
        self,
        region_code="IN",
        page_token=None
    ):

        url = f"{BASE_URL}/videos"

        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": 50,
            "key": YOUTUBE_API_KEY
        }

        if page_token:
            params["pageToken"] = page_token

        response = requests.get(url, params=params)

        response.raise_for_status()

        return response.json()

    def get_channels(self, channel_ids):

        url = f"{BASE_URL}/channels"

        params = {
            "part": "snippet,statistics",
            "id": ",".join(channel_ids),
            "maxResults": 50,
            "key": YOUTUBE_API_KEY
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        return response.json()