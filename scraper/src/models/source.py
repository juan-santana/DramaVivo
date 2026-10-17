"""Source configuration models."""

from typing import Any
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SourceConfig(BaseModel):
    """Configuration for a scraping content source."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(description="Unique identifier for the source")
    name: str = Field(description="Display name of the content provider")
    base_url: HttpUrl = Field(description="Base URL for content discovery")
    adapter_type: str = Field(description="Identifier for the adapter implementation")
    enabled: bool = Field(default=True, description="Whether this source is active for scraping")
    crawl_policy: dict[str, Any] = Field(
        default_factory=dict,
        description="Source-specific crawl settings (rate limits, headers, depth, etc.)",
    )
