"""Abstract base adapter for DramaApp scrapers."""

from abc import ABC, abstractmethod
from typing import Any
import httpx
import structlog

from src.core.security import SecurityManager
from src.models.episode import DiscoveredEpisode
from src.models.series import DiscoveredSeries
from src.models.source import SourceConfig

logger = structlog.get_logger(__name__)


class BaseAdapter(ABC):
    """Abstract base class that all source-specific adapters must implement."""

    def __init__(
        self,
        source: SourceConfig,
        http_client: httpx.AsyncClient,
        security_manager: SecurityManager | None = None,
    ):
        """
        Initialize the adapter.

        :param source: Configuration object for the target content source.
        :param http_client: Asynchronous HTTP client for requests.
        :param security_manager: Security policy and allowlist enforcer.
        """
        self.source = source
        self.client = http_client
        self.security_manager = security_manager
        self.logger = logger.bind(source_id=source.id, adapter=self.__class__.__name__)

    @abstractmethod
    async def discover_series(self) -> list[DiscoveredSeries]:
        """
        Discover and parse series from the source catalog.

        :return: List of discovered series objects.
        """
        ...

    @abstractmethod
    async def discover_episodes(self, series_url: str) -> list[DiscoveredEpisode]:
        """
        Discover and parse episodes for a specific series URL.

        :param series_url: Canonical URL of the series detail page.
        :return: List of discovered episode objects.
        """
        ...

    async def validate_source(self) -> bool:
        """
        Check if the source is accessible and permitted according to domain allowlist.

        :return: True if valid and accessible, False otherwise.
        """
        base_url_str = str(self.source.base_url)
        if self.security_manager:
            try:
                self.security_manager.validate_url(base_url_str)
            except Exception as e:
                self.logger.warning("Source URL failed security validation", error=str(e), url=base_url_str)
                return False

        # If enabled and network checking is appropriate:
        return True

    async def fetch_html(self, url: str) -> str:
        """
        Fetch HTML content from a URL after security and rate limiting checks.

        :param url: Target HTTP/HTTPS URL.
        :return: Decoded HTML string.
        """
        if self.security_manager:
            self.security_manager.validate_url(url)
            await self.security_manager.acquire_rate_limit(url)

        response = await self.client.get(url)
        response.raise_for_status()
        return response.text
