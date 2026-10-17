"""Tests for ScraperScheduler."""

from unittest.mock import AsyncMock
import pytest
from src.core.engine import ScrapingEngine
from src.core.scheduler import ScraperScheduler
from src.models.import_job import ImportJobResult


@pytest.mark.asyncio
class TestScraperScheduler:
    """Test scheduler initialization, execution, and lifecycle."""

    async def test_scheduler_lifecycle(self, demo_source_config):
        mock_engine = AsyncMock(spec=ScrapingEngine)
        mock_engine.run.return_value = [
            ImportJobResult(
                source_id=demo_source_config.id,
                started_at=pytest.importorskip("datetime").datetime.now(pytest.importorskip("datetime").timezone.utc),
                status="COMPLETED",
                records_discovered=10,
                records_imported=10,
            )
        ]

        scheduler = ScraperScheduler(engine=mock_engine, schedule_hours=4)
        assert scheduler.schedule_hours == 4
        assert scheduler.is_running is False

        # Start scheduler (without immediate execution to prevent async race in unit test)
        scheduler.start(run_immediately=False)
        assert scheduler.is_running is True

        # Calling start again should not raise
        scheduler.start(run_immediately=False)
        assert scheduler.is_running is True

        # Test execute job callback directly
        await scheduler._execute_job()
        assert mock_engine.run.called

        # Shutdown
        scheduler.shutdown(wait=False)
        assert scheduler.is_running is False

        # Redundant shutdown should not error
        scheduler.shutdown(wait=False)
