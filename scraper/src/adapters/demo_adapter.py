"""Demo adapter parsing local HTML fixtures for DramaApp."""

from datetime import date, datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup
import httpx
import structlog

from src.adapters.base import BaseAdapter
from src.core.security import SecurityManager
from src.models.episode import DiscoveredEpisode
from src.models.series import DiscoveredSeries
from src.models.source import SourceConfig

logger = structlog.get_logger(__name__)


class DemoAdapter(BaseAdapter):
    """
    Demo adapter that parses offline HTML fixtures.
    Does not require network access.
    """

    def __init__(
        self,
        source: SourceConfig,
        http_client: httpx.AsyncClient | None = None,
        security_manager: SecurityManager | None = None,
        fixtures_dir: Path | str | None = None,
    ):
        # Create a dummy or default client if none provided
        client = http_client or httpx.AsyncClient()
        super().__init__(source=source, http_client=client, security_manager=security_manager)

        if fixtures_dir:
            self.fixtures_dir = Path(fixtures_dir)
        else:
            # Detect default tests/fixtures directory relative to this file
            current_file = Path(__file__).resolve()
            scraper_root = current_file.parent.parent.parent
            self.fixtures_dir = scraper_root / "tests" / "fixtures"

        self.catalog_fixture_name = self.source.crawl_policy.get(
            "catalog_fixture", "demo_catalog.html"
        )
        self.series_fixture_name = self.source.crawl_policy.get(
            "series_fixture", "demo_series.html"
        )

    def _read_fixture(self, filename: str) -> str:
        """Read fixture file content from disk."""
        target_path = self.fixtures_dir / filename
        if not target_path.exists():
            # Also check crawl_policy custom path if provided
            custom_path = self.source.crawl_policy.get(filename)
            if custom_path and Path(custom_path).exists():
                target_path = Path(custom_path)
            else:
                raise FileNotFoundError(f"Fixture file not found: {target_path}")

        return target_path.read_text(encoding="utf-8")

    async def discover_series(self) -> list[DiscoveredSeries]:
        """Parse demo catalog fixture and return discovered drama series."""
        await self.validate_source()
        html = self._read_fixture(self.catalog_fixture_name)
        soup = BeautifulSoup(html, "lxml")

        results: list[DiscoveredSeries] = []
        cards = soup.find_all("article", class_="drama-card")

        now = datetime.now(timezone.utc)

        for card in cards:
            link_tag = card.find("a", class_="drama-link")
            series_url = link_tag["href"].strip() if link_tag and link_tag.has_attr("href") else None
            if not series_url:
                continue

            # Check security allowlist
            if self.security_manager:
                try:
                    self.security_manager.validate_url(series_url)
                except Exception as err:
                    self.logger.warning("Discovered URL rejected by security", url=series_url, error=str(err))
                    continue

            title_tag = card.find("h2", class_="title")
            title = title_tag.get_text(strip=True) if title_tag else "Untitled Drama"

            orig_title_tag = card.find("span", class_="original-title")
            orig_title = orig_title_tag.get_text(strip=True) if orig_title_tag else None

            synopsis_tag = card.find("p", class_="synopsis")
            synopsis = synopsis_tag.get_text(strip=True) if synopsis_tag else None

            genres: list[str] = []
            genres_tag = card.find("span", class_="genres")
            if genres_tag and genres_tag.get_text(strip=True):
                genres = [g.strip() for g in genres_tag.get_text(strip=True).split(",") if g.strip()]

            lang_tag = card.find("span", class_="language")
            language = lang_tag.get_text(strip=True) if lang_tag else "es"

            ep_count = None
            episodes_tag = card.find("span", class_="episodes")
            if episodes_tag:
                count_attr = episodes_tag.get("data-count")
                if count_attr and count_attr.isdigit():
                    ep_count = int(count_attr)

            poster_tag = card.find("img", class_="poster")
            poster_url = poster_tag["src"].strip() if poster_tag and poster_tag.has_attr("src") else None

            trailer_tag = card.find("a", class_="trailer")
            trailer_url = trailer_tag["href"].strip() if trailer_tag and trailer_tag.has_attr("href") else None

            pub_date = None
            date_tag = card.find("time", class_="pub-date")
            if date_tag and date_tag.has_attr("datetime"):
                try:
                    pub_date = date.fromisoformat(date_tag["datetime"].strip())
                except ValueError:
                    pass

            seo_title_tag = card.find("meta", attrs={"name": "seo-title"})
            seo_title = seo_title_tag.get("content") if seo_title_tag else None

            seo_desc_tag = card.find("meta", attrs={"name": "seo-description"})
            seo_description = seo_desc_tag.get("content") if seo_desc_tag else None

            series_item = DiscoveredSeries(
                source_id=self.source.id,
                source_url=series_url,
                title=title,
                original_title=orig_title,
                synopsis=synopsis,
                genres=genres,
                language=language,
                episode_count=ep_count,
                poster_url=poster_url,
                trailer_url=trailer_url,
                publication_date=pub_date,
                extracted_at=now,
                seo_title=seo_title,
                seo_description=seo_description,
            )
            results.append(series_item)

        self.logger.info("Demo catalog parsed", series_count=len(results))
        return results

    async def discover_episodes(self, series_url: str) -> list[DiscoveredEpisode]:
        """Parse demo series fixture and return list of episodes."""
        if self.security_manager:
            self.security_manager.validate_url(series_url)

        html = self._read_fixture(self.series_fixture_name)
        soup = BeautifulSoup(html, "lxml")

        episodes: list[DiscoveredEpisode] = []
        episode_items = soup.find_all("li", class_="episode-item")

        # Determine season number
        season_num = 1
        list_container = soup.find("ol", class_="episode-list")
        if list_container and list_container.has_attr("data-season"):
            try:
                season_num = int(list_container["data-season"])
            except ValueError:
                season_num = 1

        for item in episode_items:
            # Episode number
            ep_num = None
            if item.has_attr("data-episode-number"):
                try:
                    ep_num = int(item["data-episode-number"])
                except ValueError:
                    pass

            if ep_num is None:
                num_tag = item.find("span", class_="ep-number")
                if num_tag and num_tag.get_text(strip=True).isdigit():
                    ep_num = int(num_tag.get_text(strip=True))

            if ep_num is None:
                continue

            title_tag = item.find("h3", class_="ep-title")
            title = title_tag.get_text(strip=True) if title_tag else f"Episodio {ep_num}"

            synopsis_tag = item.find("p", class_="ep-synopsis")
            synopsis = synopsis_tag.get_text(strip=True) if synopsis_tag else None

            duration_seconds = None
            duration_tag = item.find("span", class_="ep-duration")
            if duration_tag and duration_tag.has_attr("data-seconds"):
                try:
                    duration_seconds = int(duration_tag["data-seconds"])
                except ValueError:
                    pass

            thumb_tag = item.find("img", class_="ep-thumbnail")
            thumb_url = thumb_tag["src"].strip() if thumb_tag and thumb_tag.has_attr("src") else None

            video_tag = item.find("a", class_="ep-video")
            video_url = video_tag["href"].strip() if video_tag and video_tag.has_attr("href") else None

            episode_item = DiscoveredEpisode(
                series_source_url=series_url,
                season_number=season_num,
                episode_number=ep_num,
                title=title,
                synopsis=synopsis,
                duration_seconds=duration_seconds,
                thumbnail_url=thumb_url,
                source_video_url=video_url,
            )
            episodes.append(episode_item)

        self.logger.info("Demo episodes parsed", series_url=series_url, episode_count=len(episodes))
        return episodes
