"""Backend API exporter for DramaApp."""

from typing import Sequence
import httpx
import structlog

from src.models.episode import DiscoveredEpisode
from src.models.import_job import ImportJobResult
from src.models.rights import ContentRights
from src.models.series import DiscoveredSeries

logger = structlog.get_logger(__name__)


class ApiExportError(Exception):
    """Raised when communication with backend API fails."""


class ApiExporter:
    """Exports scraped series and episodes to the DramaApp backend REST API."""

    def __init__(
        self,
        api_url: str,
        api_key: str = "",
        client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.client = client
        self.timeout = timeout

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DramaAppScraper-Exporter/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["X-API-Key"] = self.api_key
        return headers

    async def _request(self, method: str, endpoint: str, json_data: dict | list) -> dict:
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()

        if self.client:
            resp = await self.client.request(
                method, url, json=json_data, headers=headers, timeout=self.timeout
            )
        else:
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method, url, json=json_data, headers=headers, timeout=self.timeout
                )

        if resp.status_code >= 400:
            logger.error("API export request failed", status=resp.status_code, text=resp.text, url=url)
            raise ApiExportError(f"API request to {url} failed with status {resp.status_code}: {resp.text}")

        try:
            return resp.json()
        except Exception:
            return {"status": "ok", "status_code": resp.status_code}

    async def export_batch(
        self,
        source_id: str,
        series_list: Sequence[DiscoveredSeries],
        episodes_list: Sequence[DiscoveredEpisode],
        rights_list: Sequence[ContentRights] | None = None,
    ) -> dict:
        """
        Send a consolidated payload of series and episodes to the ingest endpoint.
        """
        payload = {
            "source_id": source_id,
            "series": [s.model_dump(mode="json") for s in series_list],
            "episodes": [e.model_dump(mode="json") for e in episodes_list],
            "rights": [r.model_dump(mode="json") for r in (rights_list or [])],
        }

        logger.info(
            "Exporting batch to backend API",
            url=f"{self.api_url}/import/ingest",
            series=len(series_list),
            episodes=len(episodes_list),
        )
        return await self._request("POST", "import/ingest", payload)

    async def export_series(self, series_list: Sequence[DiscoveredSeries]) -> dict:
        """Export series list to /series/batch endpoint."""
        payload = {"items": [s.model_dump(mode="json") for s in series_list]}
        return await self._request("POST", "series/batch", payload)

    async def export_episodes(self, episodes_list: Sequence[DiscoveredEpisode]) -> dict:
        """Export episodes list to /episodes/batch endpoint."""
        payload = {"items": [e.model_dump(mode="json") for e in episodes_list]}
        return await self._request("POST", "episodes/batch", payload)

    async def report_job_result(self, result: ImportJobResult) -> dict:
        """Send import job metrics and status to /import/jobs endpoint."""
        payload = result.model_dump(mode="json")
        return await self._request("POST", "import/jobs", payload)
