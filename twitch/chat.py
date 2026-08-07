from twitchAPI.chat import Chat

from utils.logger import get_logger


class TwitchChat:

    def __init__(self, client):

        self.logger = get_logger(__name__)

        self.client = client

        self.chat: Chat | None = None

    async def connect(self):

        self.logger.info("Conectando al chat...")