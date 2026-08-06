from twitchAPI.twitch import Twitch

from config import Config
from utils.logger import get_logger


class TwitchClient:

    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)

        self.client: Twitch | None = None

    async def connect(self):
        self.logger.info("Conectando con Twitch...")

    async def disconnect(self):
        self.logger.info("Desconectando...")