from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


LlmProvider = Literal["offline", "gemini", "ollama", "openai_compat"]


class Settings(BaseSettings):
    """Runtime configuration for Python Terminal Quest."""

    model_config = SettingsConfigDict(
        env_prefix="PYQUEST_",
        env_file=".env",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = 8080
    db_path: Path = Field(default_factory=lambda: Path.home() / ".pyquest" / "progress.db")
    curriculum_dir: Path = Field(default_factory=lambda: _default_repo_root() / "curriculum")
    web_dist_dir: Path = Field(default_factory=lambda: _default_repo_root() / "web" / "dist")
    standard_timeout_seconds: int = 15
    web_timeout_seconds: int = 25

    llm_provider: LlmProvider = "offline"
    llm_api_key: str = ""
    llm_model: str = ""
    llm_base_url: str = ""
    llm_timeout_seconds: float = 12.0
