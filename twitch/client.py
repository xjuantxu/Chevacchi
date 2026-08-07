from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, AuthType
from twitchAPI.type import InvalidTokenException
from .chat import TwitchChat
from twitchAPI.type import AuthType
from twitch.scopes import SCOPES

from config import Config
from utils.logger import get_logger

class TwitchClient:

    def __init__(self, config: Config):
        self.logger = get_logger(__name__)

        self.config = config
        self.chat = TwitchChat(self)

        self.api: Twitch | None = None
        self.user = None

    async def connect(self):

        self.logger.info("Conectando con Twitch...")

        await self._create_api()

        await self._authenticate()

        await self._load_user()

        await self.chat.connect()

        self.logger.info("Conexión completada.")

    async def disconnect(self):
        if self.api:
            await self.api.close()

    async def _create_api(self):

        self.api = await Twitch(
            self.config.client_id,
            self.config.client_secret
        )

        self.api.user_auth_refresh_callback = self._on_refresh
        

    async def _load_user(self):

        users = self.api.get_users()

        async for user in users:

            self.user = user

            self.logger.info(
                f"Conectado como {user.display_name} (@{user.login})"
            )

            return

        raise RuntimeError("No se pudo obtener la información del usuario.")

    async def _on_refresh(self, access_token, refresh_token):

        self.logger.info("Tokens renovados.")

        self.config.access_token = access_token
        self.config.refresh_token = refresh_token

        self.config.save()

    async def _authenticate(self):

        self.logger.info("Autenticando...")

        try:

            await self.api.set_user_authentication(
                self.config.access_token,
                SCOPES,
                self.config.refresh_token,
            )

            self.logger.info("Autenticación correcta.")

        except InvalidTokenException:
            self.logger.error(
                "Los tokens no son válidos. Ejecuta: python -m scripts.auth"
            )
            raise
