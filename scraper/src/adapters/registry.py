"""Adapter registry and factory for DramaApp scrapers."""

from typing import Type
import httpx
import structlog

from src.adapters.base import BaseAdapter
from src.adapters.demo_adapter import DemoAdapter
from src.core.security import SecurityManager
from src.models.source import SourceConfig

logger = structlog.get_logger(__name__)


class AdapterNotFoundError(Exception):
    """Raised when an adapter type is requested but not registered."""


class AdapterRegistry:
    """Registry maintaining available scraper adapters and their factory methods."""

    _registry: dict[str, Type[BaseAdapter]] = {}

    @classmethod
    def register(cls, adapter_type: str, adapter_cls: Type[BaseAdapter]) -> None:
        """Register a new adapter class under an identifier."""
        key = adapter_type.strip().lower()
        cls._registry[key] = adapter_cls
        logger.debug("Registered adapter", adapter_type=key, cls=adapter_cls.__name__)

    @classmethod
    def get(cls, adapter_type: str) -> Type[BaseAdapter]:
        """Retrieve an adapter class by its type name."""
        key = adapter_type.strip().lower()
        if key not in cls._registry:
            raise AdapterNotFoundError(
                f"Adapter '{adapter_type}' not found. Available adapters: {list(cls._registry.keys())}"
            )
        return cls._registry[key]

    @classmethod
    def create(
        cls,
        source: SourceConfig,
        http_client: httpx.AsyncClient | None = None,
        security_manager: SecurityManager | None = None,
        **kwargs,
    ) -> BaseAdapter:
        """
        Factory to instantiate an adapter for a given SourceConfig.

        :param source: Source configuration containing adapter_type.
        :param http_client: Async HTTP client.
        :param security_manager: Security manager for domain validation.
        :param kwargs: Additional arguments passed to adapter constructor.
        :return: Instantiated adapter implementing BaseAdapter.
        """
        adapter_cls = cls.get(source.adapter_type)
        return adapter_cls(
            source=source,
            http_client=http_client,
            security_manager=security_manager,
            **kwargs,
        )

    @classmethod
    def list_adapters(cls) -> list[str]:
        """Return list of all registered adapter identifiers."""
        return sorted(list(cls._registry.keys()))


# Pre-register built-in adapters
AdapterRegistry.register("demo", DemoAdapter)
AdapterRegistry.register("demo_adapter", DemoAdapter)
