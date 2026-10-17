"""JSON file exporter for scraped drama data."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Sequence
import structlog

from src.models.episode import DiscoveredEpisode
from src.models.rights import ContentRights
from src.models.series import DiscoveredSeries

logger = structlog.get_logger(__name__)


class JsonExporter:
    """Exports discovered drama records to local JSON files."""

    def __init__(self, output_dir: Path | str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self,
        source_id: str,
        series_list: Sequence[DiscoveredSeries],
        episodes_list: Sequence[DiscoveredEpisode],
        rights_list: Sequence[ContentRights] | None = None,
        job_metadata: dict | None = None,
    ) -> Path:
        """
        Export lists of series and episodes to a structured JSON file.

        :param source_id: Target source identifier.
        :param series_list: Sequence of discovered series.
        :param episodes_list: Sequence of discovered episodes.
        :param rights_list: Optional licensing rights data.
        :param job_metadata: Optional job run metrics.
        :return: Path to the written JSON file.
        """
        now = datetime.now(timezone.utc)
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{source_id}_{timestamp_str}.json"
        target_path = self.output_dir / filename

        payload = {
            "source_id": source_id,
            "exported_at": now.isoformat(),
            "metrics": {
                "series_count": len(series_list),
                "episodes_count": len(episodes_list),
                "rights_count": len(rights_list or []),
            },
            "job_metadata": job_metadata or {},
            "series": [s.model_dump(mode="json") for s in series_list],
            "episodes": [e.model_dump(mode="json") for e in episodes_list],
            "rights": [r.model_dump(mode="json") for r in (rights_list or [])],
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        # Also write a "latest.json" for convenient inspection
        latest_path = self.output_dir / f"{source_id}_latest.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        logger.info(
            "Exported scraped data to JSON",
            path=str(target_path),
            series=len(series_list),
            episodes=len(episodes_list),
        )
        return target_path
