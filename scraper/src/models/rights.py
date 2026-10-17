"""Rights and licensing models for drama content distribution."""

from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LicenseType(str, Enum):
    """Content distribution license types."""

    EXCLUSIVE = "exclusive"
    NON_EXCLUSIVE = "non_exclusive"
    PUBLIC_DOMAIN = "public_domain"
    CREATIVE_COMMONS = "creative_commons"
    SYNDICATED = "syndicated"


class ContentRights(BaseModel):
    """Licensing and territorial rights for drama series and episodes."""

    model_config = ConfigDict(extra="ignore")

    series_source_url: HttpUrl | str | None = Field(
        default=None,
        description="URL of the associated series or content item",
    )
    license_type: LicenseType = Field(
        default=LicenseType.NON_EXCLUSIVE,
        description="License category governing distribution",
    )
    territories: list[str] = Field(
        default_factory=lambda: ["GLOBAL"],
        description="List of ISO 3166-1 alpha-2 country codes or 'GLOBAL'",
    )
    valid_from: date | None = Field(default=None, description="Start date of rights window")
    valid_until: date | None = Field(default=None, description="End date of rights window")
    authorized_distributor: str | None = Field(
        default=None,
        description="Authorized entity or studio holding the copyright/license",
    )
    monetization_allowed: bool = Field(
        default=True,
        description="Whether commercial monetization (ads/paywall/coins) is permitted",
    )
