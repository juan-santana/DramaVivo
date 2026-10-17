"""Entry point for DramaApp Scraper."""

import argparse
import asyncio
import logging
import signal
import sys
from dotenv import load_dotenv
import structlog

from src.config import get_settings
from src.core.engine import ScrapingEngine
from src.core.scheduler import ScraperScheduler


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for the application."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


async def run_once(engine: ScrapingEngine) -> int:
    """Execute a single scraping run and print results summary."""
    logger = structlog.get_logger(__name__)
    logger.info("Executing single scrape cycle (--once mode)...")
    results = await engine.run()

    total_discovered = sum(r.records_discovered for r in results)
    total_imported = sum(r.records_imported for r in results)
    total_skipped = sum(r.records_skipped for r in results)
    has_failures = any(r.status == "FAILED" for r in results)

    logger.info(
        "Single run complete",
        jobs=len(results),
        total_discovered=total_discovered,
        total_imported=total_imported,
        total_skipped=total_skipped,
        has_failures=has_failures,
    )

    for r in results:
        status_marker = "[OK]" if r.status in ("COMPLETED", "PARTIAL") else "[FAIL]"
        print(
            f"{status_marker} Source: {r.source_id:<15} Status: {r.status:<10} "
            f"Discovered: {r.records_discovered:<3} Imported: {r.records_imported:<3} Skipped: {r.records_skipped:<3}"
        )
        if r.error_summary:
            print(f"      Error: {r.error_summary}")

    return 1 if has_failures else 0


async def run_scheduler(engine: ScrapingEngine, schedule_hours: int) -> None:
    """Run recurring scrape cycles using the scheduler until interrupted."""
    logger = structlog.get_logger(__name__)
    scheduler = ScraperScheduler(engine=engine, schedule_hours=schedule_hours)
    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()

    def _signal_handler():
        logger.info("Termination signal received, stopping scheduler...")
        stop_event.set()

    # Register OS signals if supported (Unix / Windows handles SIGINT via KeyboardInterrupt)
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _signal_handler)
        except (NotImplementedError, AttributeError):
            # Windows does not support add_signal_handler for all signals
            pass

    scheduler.start(run_immediately=True)
    logger.info("Scraper scheduler is running. Press Ctrl+C to exit.")

    try:
        await stop_event.wait()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        scheduler.shutdown(wait=True)


def parse_args() -> argparse.Namespace:
    """Parse command line flags."""
    parser = argparse.ArgumentParser(description="DramaApp Scraper Orchestrator")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run scraping job once and exit immediately",
    )
    parser.add_argument(
        "--schedule-hours",
        type=int,
        default=None,
        help="Override interval hours for scheduled scraper runs",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=None,
        help="Override logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    return parser.parse_args()


def main() -> None:
    """Application main entry point."""
    load_dotenv()
    args = parse_args()
    settings = get_settings()

    log_level = args.log_level or settings.log_level
    setup_logging(log_level)

    schedule_hours = args.schedule_hours or settings.schedule_hours
    engine = ScrapingEngine(settings=settings)

    if args.once:
        exit_code = asyncio.run(run_once(engine))
        sys.exit(exit_code)
    else:
        try:
            asyncio.run(run_scheduler(engine, schedule_hours))
        except KeyboardInterrupt:
            print("\nScraper stopped by user.")


if __name__ == "__main__":
    main()
