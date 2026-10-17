"""Pytest fixtures for DramaApp scraper test suite."""

import json
from pathlib import Path
import pytest

from src.core.security import SecurityManager
from src.models.source import SourceConfig


@pytest.fixture
def fixtures_dir() -> Path:
    """Return absolute path to tests/fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def catalog_html(fixtures_dir: Path) -> str:
    """Load sample catalog HTML fixture."""
    return (fixtures_dir / "demo_catalog.html").read_text(encoding="utf-8")


@pytest.fixture
def series_html(fixtures_dir: Path) -> str:
    """Load sample series HTML fixture."""
    return (fixtures_dir / "demo_series.html").read_text(encoding="utf-8")


@pytest.fixture
def demo_data(fixtures_dir: Path) -> dict:
    """Load expected parsed JSON fixture."""
    return json.loads((fixtures_dir / "demo_data.json").read_text(encoding="utf-8"))


@pytest.fixture
def demo_source_config() -> SourceConfig:
    """Return standard demo source configuration for tests."""
    return SourceConfig(
        id="demo_source",
        name="Demo Drama Catalog",
        base_url="https://demo.dramaapp.local",
        adapter_type="demo",
        enabled=True,
        crawl_policy={
            "catalog_fixture": "demo_catalog.html",
            "series_fixture": "demo_series.html",
        },
    )


@pytest.fixture
def security_manager() -> SecurityManager:
    """Return standard security manager with allowed demo domains."""
    return SecurityManager(
        allowed_domains=["demo.dramaapp.local", "example.com", "shortdrama.local"],
        default_rate_limit_delay=0.01,
        enforce_robots_txt=True,
    )
