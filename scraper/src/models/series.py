"""Discovered drama series model."""

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class DiscoveredSeries(BaseModel):
    """Metadata for a discovered drama series."""

    model_config = ConfigDict(extra="ignore")

    source_id: str = Field(description="ID of the source where the series was found")
    source_url: HttpUrl = Field(description="Canonical URL of the drama series on the source")
    title: str = Field(description="Display title of the series")
    original_title: str | None = Field(default=None, description="Original title in native script/language")
    synopsis: str | None = Field(default=None, description="Synopsis or summary of the plot")
    genres: list[str] = Field(default_factory=list, description="Genre tags (e.g. Romance, CEO, Revenge)")
    language: str = Field(default="es", description="Primary audio/subtitle language code (ISO 639-1)")
    episode_count: int | None = Field(default=None, description="Reported total number of episodes")
    poster_url: str | None = Field(default=None, description="Poster image URL")
    trailer_url: str | None = Field(default=None, description="Preview/trailer video URL")
    publication_date: date | None = Field(default=None, description="Release or publication date")
    extracted_at: datetime = Field(description="Timestamp when scraping occurred")
    seo_title: str | None = Field(default=None, description="Optimized title for search indexing")
    seo_description: str | None = Field(default=None, description="Optimized description for search indexing")
