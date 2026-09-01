from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppPaths:
    """Application filesystem paths."""

    def __init__(self) -> None:
        self.backend_dir = Path(__file__).resolve().parents[1]
        self.repo_root = self.backend_dir.parent

        # Project directories
        self.data_dir = self.backend_dir / "data"
        self.docs_dir = self.data_dir / "docs"
        self.rag_dir = self.data_dir / "rag"

        # Files
        self.catalog_path = self.data_dir / "catalog.json"
        self.context_path = self.data_dir / "context.md"

        # Frontend
        self.frontend_dir = self.repo_root / "voice-agent-frontend"

    def __repr__(self) -> str:
        return (
            f"AppPaths("
            f"backend={self.backend_dir}, "
            f"data={self.data_dir}, "
            f"frontend={self.frontend_dir}"
            f")"
        )


class Settings(BaseSettings):
    """Application settings loaded from .env."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API keys
    openai_api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )

    gemini_api_key: str | None = Field(
        default=None,
        validation_alias="GEMINI_API_KEY",
    )

    elevenlabs_api_key: str | None = Field(
        default=None,
        validation_alias="ELEVENLABS_API_KEY",
    )

    # Application
    embedding_profile: Literal["light", "rich"] = Field(
        default="light",
        validation_alias="EMBEDDING_PROFILE",
    )


class KeyRegistry:
    """Manages API-key availability."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def is_available(self, name: str) -> bool:
        keys = {
            "openai": self.settings.openai_api_key,
            "gemini": self.settings.gemini_api_key,
            "elevenlabs": self.settings.elevenlabs_api_key,
        }

        return bool(keys.get(name))

    def available(self) -> dict[str, bool]:
        return {
            name: self.is_available(name)
            for name in (
                "openai",
                "gemini",
                "elevenlabs",
            )
        }


class AppConfig:
    """Main application configuration."""

    def __init__(self) -> None:
        self.settings = Settings()
        self.paths = AppPaths()
        self.keys = KeyRegistry(self.settings)

    @property
    def embedding_profile(self) -> str:
        return self.settings.embedding_profile


# Global configuration object
config = AppConfig()