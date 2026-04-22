from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

import os

load_dotenv()


@dataclass
class TelegramConfig:
    api_id: int
    api_hash: str
    session_name: str


@dataclass
class DatabaseConfig:
    db_host: str
    db_port: int
    db_name: str
    db_password: str
    db_user: str


@dataclass
class AppConfig:
    telegram: TelegramConfig
    database: DatabaseConfig
    channels_file: str
    post_limit: int = 10
    
    
@lru_cache
def load_config() -> AppConfig:
    return AppConfig(
        channels_file=os.getenv("CHANNELS_FILE", "channels.txt"),
        post_limit=int(os.getenv("POSTS_LIMIT", "10")),
        telegram=TelegramConfig(
            api_id=int(os.getenv("TG_API_ID")),
            api_hash=os.getenv("TG_API_HASH"),
            session_name=os.getenv("TG_SESSION_NAME", "parser_session"),
        ),
        database=DatabaseConfig(
            db_port=int(os.getenv("DB_PORT")),
            db_name=os.getenv("DB_NAME"),
            db_host=os.getenv("DB_HOST"),
            db_password=os.getenv("DB_PASSWORD"),
            db_user=os.getenv("DB_USER"),
        )
    )