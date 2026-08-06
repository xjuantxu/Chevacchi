from pathlib import Path
from dataclasses import dataclass
import os

from dotenv import load_dotenv

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Config:
    client_id: str
    client_secret: str
    bot_username: str
    access_token: str
    refresh_token: str
    channel: str

    @classmethod
    def load(cls):
        load_dotenv()

        return cls(
            client_id=os.getenv("TWITCH_CLIENT_ID", ""),
            client_secret=os.getenv("TWITCH_CLIENT_SECRET", ""),
            bot_username=os.getenv("BOT_USERNAME", ""),
            access_token=os.getenv("BOT_ACCESS_TOKEN", ""),
            refresh_token=os.getenv("BOT_REFRESH_TOKEN", ""),
            channel=os.getenv("CHANNEL", "")
        )

    def save(self):
        env_file = Path(".env")

        if not env_file.exists():
            logger.error("No se encontró el archivo .env")
            raise FileNotFoundError(".env no encontrado")

        logger.info("Actualizando tokens...")

        lines = env_file.read_text().splitlines()
        new_lines = []

        changed = False

        for line in lines:

            if line.startswith("BOT_ACCESS_TOKEN="):
                new_line = f"BOT_ACCESS_TOKEN={self.access_token}"

                if line != new_line:
                    changed = True

                line = new_line

            elif line.startswith("BOT_REFRESH_TOKEN="):
                new_line = f"BOT_REFRESH_TOKEN={self.refresh_token}"

                if line != new_line:
                    changed = True

                line = new_line

            new_lines.append(line)

        if changed:
            env_file.write_text("\n".join(new_lines) + "\n")
            logger.info("Archivo .env actualizado.")
        else:
            logger.info("Los tokens ya estaban actualizados.")