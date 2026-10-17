"""Integration tests for ScrapingEngine orchestrator."""

import json
from pathlib import Path
import httpx
import pytest
import respx

from src.config import Settings
from src.core.dedup import Deduplicator
from src.core.engine import ScrapingEngine
from src.core.security import SecurityManager
from src.exporters.api_exporter import ApiExporter
from src.exporters.json_exporter import JsonExporter
from src.models.source import SourceConfig


@pytest.mark.asyncio
class TestScrapingEngineIntegration:
    """Integration test suite for ScrapingEngine, adapters, and exporters."""

    async def test_full_engine_run_with_demo_adapter(self, tmp_path: Path, demo_source_config):
        # Configure output directory in tmp_path
        json_exporter = JsonExporter(output_dir=tmp_path)
        security_manager = SecurityManager(
            allowed_domains=["demo.dramaapp.local"],
            default_rate_limit_delay=0.0,
        )
        dedup = Deduplicator()

        settings = Settings(
            api_url="http://localhost:8000/api/v1",
            api_key="",
            output_dir=str(tmp_path),
            allowed_domains=["demo.dramaapp.local"],
        )

        engine = ScrapingEngine(
            settings=settings,
            security_manager=security_manager,
            deduplicator=dedup,
            json_exporter=json_exporter,
            api_exporter=None,
        )

        results = await engine.run([demo_source_config])

        assert len(results) == 1
        job = results[0]
        assert job.source_id == demo_source_config.id
        assert job.status == "COMPLETED"
        # 5 series + (5 series * 10 episodes each = 50 total discovered)
        # Note: 5 unique series found, for each unique series discover_episodes is called
        assert job.records_discovered == 5 + (5 * 10)  # 55
        # Deduplicator seen episodes by (series_url, season, ep_num): each series has unique series_url
        assert job.records_imported == 55
        assert job.records_skipped == 0
        assert job.completed_at is not None

        # Verify exported JSON file
        latest_file = tmp_path / f"{demo_source_config.id}_latest.json"
        assert latest_file.exists()

        data = json.loads(latest_file.read_text(encoding="utf-8"))
        assert data["source_id"] == demo_source_config.id
        assert len(data["series"]) == 5
        assert len(data["episodes"]) == 50
        assert data["metrics"]["series_count"] == 5
        assert data["metrics"]["episodes_count"] == 50

    async def test_disabled_source_skipped(self, tmp_path: Path):
        disabled_source = SourceConfig(
            id="disabled_src",
            name="Disabled Source",
            base_url="https://demo.dramaapp.local",
            adapter_type="demo",
            enabled=False,
        )

        engine = ScrapingEngine(
            settings=Settings(output_dir=str(tmp_path)),
            json_exporter=JsonExporter(output_dir=tmp_path),
        )

        results = await engine.run([disabled_source])
        assert len(results) == 0

    async def test_error_isolation_between_sources(self, tmp_path: Path, demo_source_config):
        failing_source = SourceConfig(
            id="failing_src",
            name="Failing Source",
            base_url="https://disallowed-domain-site.com",
            adapter_type="demo",
            enabled=True,
        )

        security_manager = SecurityManager(
            allowed_domains=["demo.dramaapp.local"],
            default_rate_limit_delay=0.0,
        )

        engine = ScrapingEngine(
            settings=Settings(output_dir=str(tmp_path)),
            security_manager=security_manager,
            json_exporter=JsonExporter(output_dir=tmp_path),
        )

        results = await engine.run([failing_source, demo_source_config])

        assert len(results) == 2
        failing_res = results[0]
        assert failing_res.source_id == "failing_src"
        assert failing_res.status == "FAILED"
        assert failing_res.error_summary is not None

        demo_res = results[1]
        assert demo_res.source_id == "demo_source"
        assert demo_res.status == "COMPLETED"
        assert demo_res.records_imported > 0

    @respx.mock
    async def test_api_exporter_integration(self, tmp_path: Path, demo_source_config):
        api_base = "https://mockapi.dramaapp.local/api/v1"

        # Mock the backend API batch ingest endpoint
        ingest_route = respx.post(f"{api_base}/import/ingest").respond(
            status_code=200,
            json={"status": "success", "processed_records": 55},
        )

        api_exporter = ApiExporter(
            api_url=api_base,
            api_key="secret-test-token",
        )

        engine = ScrapingEngine(
            settings=Settings(
                api_url=api_base,
                api_key="secret-test-token",
                output_dir=str(tmp_path),
                allowed_domains=["demo.dramaapp.local"],
            ),
            security_manager=SecurityManager(allowed_domains=["demo.dramaapp.local"]),
            api_exporter=api_exporter,
            json_exporter=None,
        )

        results = await engine.run([demo_source_config])

        assert len(results) == 1
        assert results[0].status == "COMPLETED"
        assert ingest_route.called
        last_request = ingest_route.calls.last.request
        assert last_request.headers["Authorization"] == "Bearer secret-test-token"
        body = json.loads(last_request.content)
        assert body["source_id"] == demo_source_config.id
        assert len(body["series"]) == 5
