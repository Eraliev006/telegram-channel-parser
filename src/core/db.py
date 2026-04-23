import asyncpg

from src.core import get_logger, Channel, Post
from src.core import DatabaseConfig

logger = get_logger(__name__)

class Database:
    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._conn: asyncpg.Connection | None = None

    async def connect(self) -> None:
        logger.info("Connect to DB")
        self._conn = await asyncpg.connect(
            user=self._config.db_user,
            password=self._config.db_password,
            database=self._config.db_name,
            host=self._config.db_host,
            port=self._config.db_port
        )

    async def init_db(self):
        await self._conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS channels (
                id UUID PRIMARY KEY,
                name VARCHAR NOT NULL,
                username VARCHAR UNIQUE NOT NULL,
                description TEXT,
                followers_count INTEGER DEFAULT 0,
                avatar_url VARCHAR,
                created_at TIMESTAMP DEFAULT NOW()
            );
            
            CREATE TABLE IF NOT EXISTS posts (
                id UUID PRIMARY KEY,
                channel_id UUID REFERENCES channels(id),
                message_id INTEGER NOT NULL,
                text TEXT,
                published_at TIMESTAMP,
                views_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                replies_count INTEGER DEFAULT 0,
                reposts_count INTEGER DEFAULT 0,
                UNIQUE (channel_id, message_id)
            );
            '''
        )
        logger.info("Tables initialized")

    async def save_channel(self, channel: Channel) -> None:
        await self._conn.execute(
            '''
                INSERT INTO channels (id, name, username, description, followers_count, avatar_url)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (username) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                followers_count = EXCLUDED.followers_count,
                avatar_url = EXCLUDED.avatar_url
            ''',
            channel.id,
            channel.name,
            channel.username,
            channel.description,
            channel.followers_count,
            channel.avatar_url
        )
        logger.info(f"Channel saved: {channel.username}")

    async def save_post(self, post: Post) -> None:
        await self._conn.execute(
            '''
            INSERT INTO posts (id,channel_id,message_id,
                text,published_at,views_count,
                comments_count,replies_count,reposts_count
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (channel_id, message_id) DO UPDATE SET
            text = EXCLUDED.text,
            published_at = EXCLUDED.published_at,
            views_count = EXCLUDED.views_count,
            comments_count = EXCLUDED.comments_count,
            replies_count = EXCLUDED.replies_count,
            reposts_count = EXCLUDED.reposts_count
            ''',
            post.id,
            post.channel_id,
            post.message_id,
            post.text,
            post.published_at,
            post.views_count,
            post.comments_count,
            post.replies_count,
            post.reposts_count
        )
        logger.info(f"Post saved: message_id={post.message_id}, channel_id={post.channel_id}")

    async def dispose(self) -> None:
        logger.info("Closing connection with DB")
        if self._conn:
            await self._conn.close()
            logger.info('Connection with DB closed')
