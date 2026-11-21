from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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
