from datetime import datetime
from typing import Optional, TypedDict


class VideoData(TypedDict):
    video_id: str
    name: str
    url: str
    channel_id: str
    channel_name: str
    timestamp: datetime
    watch_timestamp: Optional[datetime]


class ChannelData(TypedDict):
    channel_id: str
    name: str
    new_videos: dict
