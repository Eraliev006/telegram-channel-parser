from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from uuid import UUID


@dataclass
class Channel:
    id: UUID
    name: str
    username: str
    description: Optional[str] = None
    followers_count: int = 0
    avatar_url: Optional[str] = None
    created_at: datetime = None


@dataclass
class Post:
    id: UUID
    channel_id: UUID
    message_id: int
    text: Optional[str] = None
    published_at: datetime = None
    views_count: int = 0
    comments_count: int = 0
    replies_count: int = 0
    reposts_count: int = 0