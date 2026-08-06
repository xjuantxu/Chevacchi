import asyncio

from config import Config
from twitch.auth import TwitchAuthenticator
from utils.logger import get_logger

logger = get_logger(__name__)


async def main():
    logger.info("Iniciando asistente OAuth...")

    config = Config.load()

    auth = TwitchAuthenticator(config)

    success = await auth.authenticate()

    if success:
        logger.info("Autenticación completada correctamente.")
    else:
        logger.error("No se pudo completar la autenticación.")


if __name__ == "__main__":
    asyncio.run(main())