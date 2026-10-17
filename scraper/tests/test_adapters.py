"""Tests for Scraper Adapters and Registry."""

import pytest
from src.adapters.base import BaseAdapter
from src.adapters.demo_adapter import DemoAdapter
from src.adapters.registry import AdapterNotFoundError, AdapterRegistry
from src.core.security import SecurityManager
from src.models.episode import DiscoveredEpisode
from src.models.series import DiscoveredSeries
from src.models.source import SourceConfig


@pytest.mark.asyncio
class TestDemoAdapter:
    """Test DemoAdapter parsing and extraction capabilities."""

    async def test_discover_series(self, demo_source_config, security_manager, demo_data):
        adapter = DemoAdapter(
            source=demo_source_config,
            security_manager=security_manager,
        )

        series_list = await adapter.discover_series()
        assert len(series_list) == 5
        assert all(isinstance(s, DiscoveredSeries) for s in series_list)

        expected_titles = [s["title"] for s in demo_data["series"]]
        extracted_titles = [s.title for s in series_list]
        assert extracted_titles == expected_titles

        # Detailed check of first series
        first = series_list[0]
        expected_first = demo_data["series"][0]
        assert first.title == expected_first["title"]
        assert first.original_title == expected_first["original_title"]
        assert first.synopsis == expected_first["synopsis"]
        assert first.genres == expected_first["genres"]
        assert first.language == expected_first["language"]
        assert first.episode_count == expected_first["episode_count"]
        assert first.poster_url == expected_first["poster_url"]
        assert first.trailer_url == expected_first["trailer_url"]
        assert str(first.publication_date) == expected_first["publication_date"]
        assert first.seo_title == expected_first["seo_title"]
        assert first.seo_description == expected_first["seo_description"]

    async def test_discover_episodes(self, demo_source_config, security_manager, demo_data):
        adapter = DemoAdapter(
            source=demo_source_config,
            security_manager=security_manager,
        )

        series_url = "https://demo.dramaapp.local/series/el-secreto-del-multimillonario"
        episodes_list = await adapter.discover_episodes(series_url)
        assert len(episodes_list) == 10
        assert all(isinstance(e, DiscoveredEpisode) for e in episodes_list)

        # Check numbering sequence
        assert [e.episode_number for e in episodes_list] == list(range(1, 11))

        # Check first episode details
        first_ep = episodes_list[0]
        expected_first_ep = demo_data["episodes"][0]
        assert str(first_ep.series_source_url).rstrip("/") == expected_first_ep["series_source_url"]
        assert first_ep.title == expected_first_ep["title"]
        assert first_ep.synopsis == expected_first_ep["synopsis"]
        assert first_ep.duration_seconds == expected_first_ep["duration_seconds"]
        assert first_ep.thumbnail_url == expected_first_ep["thumbnail_url"]
        assert first_ep.source_video_url == expected_first_ep["source_video_url"]

    async def test_validate_source_success(self, demo_source_config, security_manager):
        adapter = DemoAdapter(
            source=demo_source_config,
            security_manager=security_manager,
        )
        is_valid = await adapter.validate_source()
        assert is_valid is True

    async def test_validate_source_disallowed_domain(self):
        source = SourceConfig(
            id="untrusted",
            name="Untrusted Source",
            base_url="https://untrusted-pirate-site.com",
            adapter_type="demo",
        )
        sec = SecurityManager(allowed_domains=["demo.dramaapp.local"])
        adapter = DemoAdapter(source=source, security_manager=sec)
        is_valid = await adapter.validate_source()
        assert is_valid is False


class TestAdapterRegistry:
    """Test AdapterRegistry lookup and factory instantiation."""

    def test_registry_contains_demo_adapter(self):
        cls = AdapterRegistry.get("demo")
        assert cls == DemoAdapter
        assert "demo" in AdapterRegistry.list_adapters()

    def test_unknown_adapter_raises_error(self):
        with pytest.raises(AdapterNotFoundError):
            AdapterRegistry.get("non_existent_adapter_type")

    def test_create_adapter_factory(self, demo_source_config, security_manager):
        adapter = AdapterRegistry.create(
            source=demo_source_config,
            security_manager=security_manager,
        )
        assert isinstance(adapter, DemoAdapter)
        assert adapter.source.id == demo_source_config.id

    def test_custom_adapter_registration(self):
        class CustomAdapter(BaseAdapter):
            async def discover_series(self):
                return []

            async def discover_episodes(self, series_url: str):
                return []

        AdapterRegistry.register("custom_test", CustomAdapter)
        assert AdapterRegistry.get("custom_test") == CustomAdapter
        assert "custom_test" in AdapterRegistry.list_adapters()
