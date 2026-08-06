import asyncio

from config import Config
from twitch.client import TwitchClient
from utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    try:
        config = Config.load()

        twitch = TwitchClient(config)

        await twitch.connect()

    except Exception:
        logger.exception("Chevacchi no pudo iniciarse.")


if __name__ == "__main__":
    asyncio.run(main())