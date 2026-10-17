"""Core scraping, security, deduplication, and scheduling engine."""

from src.core.dedup import Deduplicator, normalize_title
from src.core.engine import ScrapingEngine
from src.core.scheduler import ScraperScheduler
from src.core.security import (
    DisallowedDomainError,
    InvalidURLError,
    RobotsDisallowedError,
    SecurityError,
    SecurityManager,
)

__all__ = [
    "ScrapingEngine",
    "ScraperScheduler",
    "Deduplicator",
    "normalize_title",
    "SecurityManager",
    "SecurityError",
    "DisallowedDomainError",
    "InvalidURLError",
    "RobotsDisallowedError",
]
