"""Configuration settings for the DramaApp Scraper."""

from functools import lru_cache
from typing import Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_url: str = Field(
        default="http://localhost:8000/api/v1",
        description="Base URL for the DramaApp backend API",
    )
    api_key: str = Field(
        default="",
        description="API authentication key for backend API export",
    )
    schedule_hours: int = Field(
        default=6,
        description="Interval in hours for scheduled scraping runs",
    )
    allowed_domains: list[str] = Field(
        default_factory=lambda: [
            "example.com",
            "demo.dramaapp.local",
            "fixtures.dramaapp.local",
            "shortdrama.local",
        ],
        description="Domain allowlist for security verification",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    output_dir: str = Field(
        default="output",
        description="Directory path for local JSON exports and artifacts",
    )
    request_timeout: float = Field(
        default=30.0,
        description="Default HTTP request timeout in seconds",
    )
    user_agent: str = Field(
        default="DramaAppScraper/1.0 (+https://dramaapp.local/bot)",
        description="User-Agent header for HTTP requests",
    )

    @field_validator("allowed_domains", mode="before")
    @classmethod
    def parse_allowed_domains(cls, value: Any) -> list[str]:
        """Convert comma-separated string to list of trimmed domain strings."""
        if isinstance(value, str):
            return [d.strip().lower() for d in value.split(",") if d.strip()]
        if isinstance(value, list):
            return [str(d).strip().lower() for d in value if str(d).strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached instance of Settings."""
    return Settings()
