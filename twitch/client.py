from twitchAPI.twitch import Twitch

from config import Config
from utils.logger import get_logger

from .auth import TwitchAuthenticator


class TwitchClient:

    def __init__(self, config: Config):
        self.logger = get_logger(__name__)

        self.config = config

        self.api: Twitch | None = None
        self.user = None

        self.auth = TwitchAuthenticator(self)

    async def connect(self):

        self.logger.info("Conectando con Twitch...")

        await self._create_api()

        authenticated = await self.auth.authenticate()

        if not authenticated:
            raise RuntimeError("No se ha podido autenticar con Twitch.")

        await self._load_user()

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
        pass

    async def _on_refresh(self, access_token, refresh_token):

        self.logger.info("Tokens renovados.")

        self.config.access_token = access_token
        self.config.refresh_token = refresh_token

        self.config.save()

    async def _authorize(self) -> bool:

        self.logger.info("Entrando en _authorize()")

        try:
            self.logger.info("Creando UserAuthenticator...")

            auth = UserAuthenticator(
                self.api,
                SCOPES,
                force_verify=False
            )

            self.logger.info("Llamando a authenticate()...")

            access_token, refresh_token = await auth.authenticate()

            self.logger.info("authenticate() finalizado.")

            self.config.access_token = access_token
            self.config.refresh_token = refresh_token

            self._save_tokens()

            self.logger.info("Credenciales guardadas correctamente.")

            return True

        except Exception:
            self.logger.exception("Error durante la autorización.")
            return False
                