"""Scraping engine orchestrator for DramaApp."""

from datetime import datetime, timezone
from typing import Sequence
import httpx
import structlog

from src.adapters.base import BaseAdapter
from src.adapters.registry import AdapterRegistry
from src.config import Settings, get_settings
from src.core.dedup import Deduplicator
from src.core.security import SecurityManager
from src.exporters.api_exporter import ApiExporter
from src.exporters.json_exporter import JsonExporter
from src.models.episode import DiscoveredEpisode
from src.models.import_job import ImportJobResult
from src.models.series import DiscoveredSeries
from src.models.source import SourceConfig

logger = structlog.get_logger(__name__)


class ScrapingEngine:
    """
    Core orchestrator that runs adapters, applies security validation,
    performs deduplication, and exports results to JSON and backend API.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        security_manager: SecurityManager | None = None,
        deduplicator: Deduplicator | None = None,
        json_exporter: JsonExporter | None = None,
        api_exporter: ApiExporter | None = None,
        http_client: httpx.AsyncClient | None = None,
    ):
        self.settings = settings or get_settings()
        self.security_manager = security_manager or SecurityManager(
            allowed_domains=self.settings.allowed_domains
        )
        self.deduplicator = deduplicator or Deduplicator()
        self.json_exporter = json_exporter or JsonExporter(output_dir=self.settings.output_dir)
        self.api_exporter = api_exporter or (
            ApiExporter(api_url=self.settings.api_url, api_key=self.settings.api_key)
            if self.settings.api_key
            else None
        )
        self._client = http_client

    def get_default_sources(self) -> list[SourceConfig]:
        """Return default configured sources, including demo adapter."""
        return [
            SourceConfig(
                id="demo_source",
                name="Demo Drama Catalog",
                base_url="https://demo.dramaapp.local",
                adapter_type="demo",
                enabled=True,
                crawl_policy={"catalog_fixture": "demo_catalog.html", "series_fixture": "demo_series.html"},
            )
        ]

    async def run_source(
        self, source: SourceConfig, client: httpx.AsyncClient
    ) -> ImportJobResult:
        """
        Execute scraping pipeline for a single source.
        Gracefully handles errors so that individual source failures do not halt the system.
        """
        started_at = datetime.now(timezone.utc)
        job = ImportJobResult(
            source_id=source.id,
            started_at=started_at,
            status="RUNNING",
            records_discovered=0,
            records_imported=0,
            records_skipped=0,
        )

        log = logger.bind(source_id=source.id, adapter=source.adapter_type)
        log.info("Starting scrape job for source")

        all_unique_series: list[DiscoveredSeries] = []
        all_unique_episodes: list[DiscoveredEpisode] = []
        total_discovered = 0
        total_skipped = 0
        had_partial_errors = False

        try:
            adapter = AdapterRegistry.create(
                source=source,
                http_client=client,
                security_manager=self.security_manager,
            )

            # Validate source base_url
            if not await adapter.validate_source():
                raise ValueError(f"Source validation failed for base_url: {source.base_url}")

            # 1. Discover Series
            raw_series = await adapter.discover_series()
            total_discovered += len(raw_series)

            # Deduplicate series
            unique_series, dup_series = self.deduplicator.deduplicate_series(raw_series)
            total_skipped += len(dup_series)
            all_unique_series.extend(unique_series)

            # 2. Discover Episodes for each unique series
            for s in unique_series:
                series_url_str = str(s.source_url)
                try:
                    raw_episodes = await adapter.discover_episodes(series_url_str)
                    total_discovered += len(raw_episodes)

                    unique_ep, dup_ep = self.deduplicator.deduplicate_episodes(raw_episodes)
                    total_skipped += len(dup_ep)
                    all_unique_episodes.extend(unique_ep)
                except Exception as ep_err:
                    had_partial_errors = True
                    log.warning(
                        "Error discovering episodes for series",
                        series_url=series_url_str,
                        error=str(ep_err),
                    )

            # 3. Export data
            total_imported = len(all_unique_series) + len(all_unique_episodes)

            # Export to JSON
            if self.json_exporter:
                self.json_exporter.export(
                    source_id=source.id,
                    series_list=all_unique_series,
                    episodes_list=all_unique_episodes,
                    job_metadata={"partial_errors": had_partial_errors},
                )

            # Export to API if configured
            if self.api_exporter:
                try:
                    await self.api_exporter.export_batch(
                        source_id=source.id,
                        series_list=all_unique_series,
                        episodes_list=all_unique_episodes,
                    )
                except Exception as api_err:
                    log.error("Failed exporting to backend API", error=str(api_err))
                    had_partial_errors = True

            job.records_discovered = total_discovered
            job.records_imported = total_imported
            job.records_skipped = total_skipped
            job.status = "PARTIAL" if had_partial_errors else "COMPLETED"
            job.completed_at = datetime.now(timezone.utc)
            log.info(
                "Scrape job completed",
                status=job.status,
                discovered=total_discovered,
                imported=total_imported,
                skipped=total_skipped,
            )

        except Exception as e:
            job.status = "FAILED"
            job.error_summary = str(e)
            job.completed_at = datetime.now(timezone.utc)
            log.error("Scrape job failed", error=str(e), exc_info=True)

        return job

    async def run(
        self, sources: Sequence[SourceConfig] | None = None
    ) -> list[ImportJobResult]:
        """
        Run the scrape pipeline across all provided or default sources.
        """
        target_sources = list(sources) if sources is not None else self.get_default_sources()
        enabled_sources = [s for s in target_sources if s.enabled]

        logger.info("Executing engine scrape run", total_sources=len(enabled_sources))
        results: list[ImportJobResult] = []

        if self._client:
            for source in enabled_sources:
                res = await self.run_source(source, self._client)
                results.append(res)
        else:
            async with httpx.AsyncClient(timeout=self.settings.request_timeout) as client:
                for source in enabled_sources:
                    res = await self.run_source(source, client)
                    results.append(res)

        return results
