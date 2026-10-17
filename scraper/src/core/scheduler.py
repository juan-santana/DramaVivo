"""APScheduler integration for recurring DramaApp scrape jobs."""

import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import structlog

from src.config import Settings, get_settings
from src.core.engine import ScrapingEngine

logger = structlog.get_logger(__name__)


class ScraperScheduler:
    """Manages scheduled background execution of the scraping engine."""

    def __init__(
        self,
        engine: ScrapingEngine | None = None,
        settings: Settings | None = None,
        schedule_hours: int | None = None,
    ):
        self.settings = settings or get_settings()
        self.engine = engine or ScrapingEngine(settings=self.settings)
        self.schedule_hours = schedule_hours or self.settings.schedule_hours
        self.scheduler = AsyncIOScheduler()
        self._is_running = False

    async def _execute_job(self) -> None:
        """Internal callback executed by the scheduler."""
        logger.info("Scheduler triggered scraping cycle", timestamp=datetime.now(timezone.utc).isoformat())
        try:
            results = await self.engine.run()
            for res in results:
                logger.info(
                    "Job execution result",
                    source=res.source_id,
                    status=res.status,
                    imported=res.records_imported,
                    discovered=res.records_discovered,
                    skipped=res.records_skipped,
                )
        except Exception as e:
            logger.error("Error during scheduled scraping run", error=str(e), exc_info=True)

    def start(self, run_immediately: bool = True) -> None:
        """
        Start the scheduler with the configured interval trigger.

        :param run_immediately: Whether to trigger a run at startup.
        """
        if self._is_running:
            logger.warning("Scheduler is already running.")
            return

        trigger = IntervalTrigger(hours=self.schedule_hours)
        next_run_time = datetime.now() if run_immediately else None

        self.scheduler.add_job(
            self._execute_job,
            trigger=trigger,
            id="dramaapp_scraper_job",
            name="DramaApp Periodic Scrape",
            replace_existing=True,
            next_run_time=next_run_time,
        )

        self.scheduler.start()
        self._is_running = True
        logger.info(
            "Scheduler started successfully",
            interval_hours=self.schedule_hours,
            run_immediately=run_immediately,
        )

    def shutdown(self, wait: bool = True) -> None:
        """Gracefully shut down the scheduler."""
        if not self._is_running:
            return

        logger.info("Shutting down scraper scheduler...")
        self.scheduler.shutdown(wait=wait)
        self._is_running = False
        logger.info("Scheduler stopped.")

    @property
    def is_running(self) -> bool:
        """Check if scheduler is currently active."""
        return self._is_running
