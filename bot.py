import asyncio

from config import Config
from twitch.client import TwitchClient
from utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    logger.info("Iniciando Chevacchi...")

    config = Config.load()

    twitch = TwitchClient(config)

    await twitch.connect()


if __name__ == "__main__":
    asyncio.run(main())