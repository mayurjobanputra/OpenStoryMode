# Configuration loading for OpenStoryMode

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment variables or .env file."""

    openrouter_api_key: str
    port: int

    @property
    def api_key_configured(self) -> bool:
        """Return True iff openrouter_api_key is a non-empty, non-whitespace string."""
        return bool(self.openrouter_api_key and self.openrouter_api_key.strip())

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment variables."""
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        port = int(os.environ.get("PORT", "8000"))
        return cls(openrouter_api_key=api_key, port=port)


def validate_config(config: Config) -> None:
    """Validate configuration values and log warnings for missing settings."""
    if not config.api_key_configured:
        logger.warning(
            "OPENROUTER_API_KEY is not set. Video generation is disabled. "
            "Set the OPENROUTER_API_KEY environment variable and restart."
        )


config = Config.load()
