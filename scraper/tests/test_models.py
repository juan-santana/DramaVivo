"""Tests for Pydantic models in DramaApp scraper."""

from datetime import date, datetime, timezone
import pytest
from pydantic import ValidationError

from src.models.episode import DiscoveredEpisode
from src.models.import_job import ImportJobResult
from src.models.rights import ContentRights, LicenseType
from src.models.series import DiscoveredSeries
from src.models.source import SourceConfig


class TestSourceConfigModel:
    """Test SourceConfig Pydantic model validation."""

    def test_valid_source_config(self):
        source = SourceConfig(
            id="src_1",
            name="Source One",
            base_url="https://example.com/api",
            adapter_type="demo",
            enabled=True,
            crawl_policy={"rate_limit": 2.0},
        )
        assert source.id == "src_1"
        assert str(source.base_url) == "https://example.com/api"
        assert source.adapter_type == "demo"
        assert source.enabled is True
        assert source.crawl_policy["rate_limit"] == 2.0

    def test_invalid_base_url(self):
        with pytest.raises(ValidationError):
            SourceConfig(
                id="src_bad",
                name="Bad Source",
                base_url="not-a-valid-url",
                adapter_type="demo",
            )

    def test_default_values(self):
        source = SourceConfig(
            id="src_defaults",
            name="Defaults Source",
            base_url="https://example.com",
            adapter_type="demo",
        )
        assert source.enabled is True
        assert source.crawl_policy == {}


class TestDiscoveredSeriesModel:
    """Test DiscoveredSeries Pydantic model validation."""

    def test_valid_series(self):
        series = DiscoveredSeries(
            source_id="src_1",
            source_url="https://demo.dramaapp.local/series/test-drama",
            title="Test Drama Title",
            original_title="Original Drama Title",
            synopsis="A short description of the drama plot.",
            genres=["Romance", "Drama"],
            language="es",
            episode_count=10,
            poster_url="https://demo.dramaapp.local/posters/test.jpg",
            trailer_url="https://demo.dramaapp.local/trailers/test.mp4",
            publication_date=date(2026, 1, 15),
            extracted_at=datetime.now(timezone.utc),
            seo_title="Test Drama SEO",
            seo_description="Test Drama SEO Description",
        )
        assert series.title == "Test Drama Title"
        assert len(series.genres) == 2
        assert series.publication_date == date(2026, 1, 15)

    def test_minimal_series(self):
        now = datetime.now(timezone.utc)
        series = DiscoveredSeries(
            source_id="src_min",
            source_url="https://example.com/drama-1",
            title="Minimal Drama",
            extracted_at=now,
        )
        assert series.language == "es"
        assert series.genres == []
        assert series.episode_count is None
        assert series.poster_url is None

    def test_invalid_series_url(self):
        with pytest.raises(ValidationError):
            DiscoveredSeries(
                source_id="src_err",
                source_url="ftp://invalid-scheme.com",  # HttpUrl requires http or https
                title="Bad URL Drama",
                extracted_at=datetime.now(timezone.utc),
            )


class TestDiscoveredEpisodeModel:
    """Test DiscoveredEpisode Pydantic model validation."""

    def test_valid_episode(self):
        ep = DiscoveredEpisode(
            series_source_url="https://demo.dramaapp.local/series/drama-1",
            season_number=1,
            episode_number=5,
            title="Episode 5 Title",
            synopsis="Plot of ep 5",
            duration_seconds=120,
            thumbnail_url="https://demo.dramaapp.local/thumbs/ep5.jpg",
            source_video_url="https://demo.dramaapp.local/media/ep5.m3u8",
        )
        assert ep.episode_number == 5
        assert ep.season_number == 1
        assert ep.duration_seconds == 120

    def test_invalid_episode_number(self):
        with pytest.raises(ValidationError):
            # episode_number must be >= 1
            DiscoveredEpisode(
                series_source_url="https://demo.dramaapp.local/series/drama-1",
                episode_number=0,
                title="Invalid Ep Number",
            )

    def test_invalid_negative_duration(self):
        with pytest.raises(ValidationError):
            DiscoveredEpisode(
                series_source_url="https://demo.dramaapp.local/series/drama-1",
                episode_number=1,
                title="Invalid Duration",
                duration_seconds=-10,
            )


class TestImportJobResultModel:
    """Test ImportJobResult Pydantic model validation."""

    def test_valid_job_result(self):
        started = datetime.now(timezone.utc)
        job = ImportJobResult(
            source_id="src_test",
            started_at=started,
            status="COMPLETED",
            records_discovered=15,
            records_imported=15,
            records_skipped=0,
        )
        assert job.status == "COMPLETED"
        assert job.records_discovered == 15
        assert job.completed_at is None

    def test_invalid_status_literal(self):
        with pytest.raises(ValidationError):
            ImportJobResult(
                source_id="src_test",
                started_at=datetime.now(timezone.utc),
                status="INVALID_STATUS",  # Must be RUNNING, COMPLETED, FAILED, PARTIAL
            )

    def test_status_literals(self):
        now = datetime.now(timezone.utc)
        for valid_status in ["RUNNING", "COMPLETED", "FAILED", "PARTIAL"]:
            job = ImportJobResult(
                source_id="src_1",
                started_at=now,
                status=valid_status,
            )
            assert job.status == valid_status


class TestContentRightsModel:
    """Test ContentRights Pydantic model validation."""

    def test_default_rights(self):
        rights = ContentRights(series_source_url="https://demo.dramaapp.local/series/drama-1")
        assert rights.license_type == LicenseType.NON_EXCLUSIVE
        assert rights.territories == ["GLOBAL"]
        assert rights.monetization_allowed is True

    def test_custom_rights(self):
        rights = ContentRights(
            series_source_url="https://demo.dramaapp.local/series/drama-1",
            license_type=LicenseType.EXCLUSIVE,
            territories=["US", "MX", "ES"],
            valid_from=date(2026, 1, 1),
            valid_until=date(2027, 1, 1),
            authorized_distributor="DramaApp Studio",
            monetization_allowed=True,
        )
        assert rights.license_type == LicenseType.EXCLUSIVE
        assert len(rights.territories) == 3
        assert rights.authorized_distributor == "DramaApp Studio"
