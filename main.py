import argparse
import asyncio

from src.core import load_config, get_db, get_logger
from src.parser import Parser

logger = get_logger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channels", type=int, default=None)
    parser.add_argument("--posts", type=int, default=None)
    logger.info('Parse args from CLI')
    return parser.parse_args()

async def main():
    args = parse_args()
    config = load_config()
    logger.info('Load config: %s', config)

    async with get_db(config.database) as db:
        parser = Parser(config, db)
        await parser.run(
            post_limit=args.posts,
            channel_limit=args.channels
        )

asyncio.run(main())