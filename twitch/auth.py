from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope
from twitch.scopes import SCOPES

from config import Config
from utils.logger import get_logger




class TwitchAuthenticator:

    def __init__(self, config: Config):
        self.logger = get_logger(__name__)

        self.config = config

        self.api: Twitch | None = None

    async def authenticate(self) -> bool:

        self.logger.info("Iniciando autenticación...")

        await self._create_api()

        return await self._authorize()

    async def _create_api(self):

        self.api = await Twitch(
            self.config.client_id,
            self.config.client_secret,
        )

        self.api.user_auth_refresh_callback = self._on_refresh

    async def _authorize(self) -> bool:
        try:
            self.logger.info("Abriendo asistente OAuth...")

            authenticator = UserAuthenticator(
                self.api,
                SCOPES,
                force_verify=False
            )

            access_token, refresh_token = await authenticator.authenticate()

            self.config.access_token = access_token
            self.config.refresh_token = refresh_token

            self._save_tokens()

            self.logger.info("Credenciales guardadas correctamente.")

            return True

        except Exception:
            self.logger.exception("Error durante la autorización.")
            return False

    async def _on_refresh(self, access_token: str, refresh_token: str):

        self.logger.info("Tokens renovados.")

        self.config.access_token = access_token
        self.config.refresh_token = refresh_token

        self._save_tokens()

    def _save_tokens(self):

        self.config.save()