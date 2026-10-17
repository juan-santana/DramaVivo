"""Discovered drama episode model."""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class DiscoveredEpisode(BaseModel):
    """Metadata for a single episode of a drama series."""

    model_config = ConfigDict(extra="ignore")

    series_source_url: HttpUrl = Field(description="URL of the parent drama series")
    season_number: int = Field(default=1, ge=1, description="Season number (default: 1)")
    episode_number: int = Field(ge=1, description="Episode sequence number (1-indexed)")
    title: str = Field(description="Episode title")
    synopsis: str | None = Field(default=None, description="Episode synopsis or short description")
    duration_seconds: int | None = Field(default=None, ge=0, description="Episode duration in seconds")
    thumbnail_url: str | None = Field(default=None, description="Episode preview thumbnail URL")
    source_video_url: str | None = Field(
        default=None,
        description="Stream or media URL (only populated if from authorized source)",
    )
