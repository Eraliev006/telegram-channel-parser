import asyncio
from uuid import uuid4

from telethon import TelegramClient
from telethon.errors import FloodWaitError

from src.core.config import AppConfig
from src.core import Database, get_logger, Channel, Post

logger = get_logger(__name__)

class Parser:
    def __init__(self, config: AppConfig, db: Database) -> None:
        self._db = db
        self._config = config
        self._client = TelegramClient(
            config.telegram.session_name,
            config.telegram.api_id,
            config.telegram.api_hash
        )

    async def parse_channel(self, username: str, post_limit: int | None= None) -> None:
        post_limit = post_limit if post_limit else self._config.post_limit
        try:
            channel = await self._client.get_entity(username)
            channel_obj = Channel(
                id=uuid4(),
                name=channel.title,
                username=channel.username,
                description=getattr(channel, 'about', None),
                followers_count=channel.participants_count,
                avatar_url=None,
            )

            logger.info('Parsed channel: @%s, subscribers: %d', channel_obj.username, channel_obj.followers_count or 0)
            await self._db.save_channel(channel_obj)

            messages = await self._client.get_messages(username, limit=post_limit)
            for message in messages:
                post_obj = Post(
                    id=uuid4(),
                    channel_id=channel_obj.id,
                    message_id=message.id,
                    text=message.text,
                    published_at=message.date,
                    views_count=message.views or 0,
                    comments_count=message.replies.replies if message.replies else 0,
                    replies_count=0,
                    reposts_count=message.forwards or 0,
                )

                await self._db.save_post(post_obj)

        except FloodWaitError as e:
            logger.warning(f"FloodWait: sleeping {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            await self.parse_channel(username)

        except Exception as e:
            logger.error(f"Error parsing {username}: {e}")


    async def run(self, post_limit: int | None=None, channel_limit: int | None =None) -> None:
        logger.info('Start parsing')
        async with self._client:
            with open(self._config.channels_file, "r") as f:
                logger.debug('File with data: %s', self._config.channels_file)
                usernames = [line.strip() for line in f if line.strip()]
                if channel_limit:
                    usernames = usernames[:channel_limit]

            for username in usernames:
                await self.parse_channel(username, post_limit=post_limit)
                await asyncio.sleep(2)

        logger.info('End parsing')

