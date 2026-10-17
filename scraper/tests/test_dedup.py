"""Tests for Deduplication logic."""

from datetime import datetime, timezone
import pytest
from src.core.dedup import Deduplicator, normalize_title
from src.models.episode import DiscoveredEpisode
from src.models.series import DiscoveredSeries


class TestNormalizeTitle:
    """Test title normalization logic."""

    def test_lowercase_and_accents(self):
        assert normalize_title("El Secreto del Multimillonario") == "el secreto del multimillonario"
        assert normalize_title("Pasión, Traición & Venganza") == "pasion traicion venganza"

    def test_strip_punctuation_and_whitespace(self):
        assert normalize_title("  Drama:   Amor / Dolor !! ") == "drama amor dolor"
        assert normalize_title("") == ""

    def test_spanish_tildes(self):
        assert normalize_title("La Niña del Río") == "la nina del rio"


class TestDeduplicator:
    """Test Deduplicator class methods."""

    def test_mark_and_is_url_seen(self):
        dedup = Deduplicator()
        url1 = "https://demo.dramaapp.local/series/1"
        url1_slash = "https://demo.dramaapp.local/series/1/"

        assert dedup.is_url_seen(url1) is False
        assert dedup.mark_url_seen(url1) is True

        # Second time should be seen
        assert dedup.is_url_seen(url1) is True
        assert dedup.mark_url_seen(url1) is False

        # Trailing slash should be treated as duplicate
        assert dedup.is_url_seen(url1_slash) is True
        assert dedup.mark_url_seen(url1_slash) is False

    def test_calculate_title_similarity(self):
        dedup = Deduplicator()
        assert dedup.calculate_title_similarity("El Secreto", "El Secreto") == 1.0
        assert dedup.calculate_title_similarity("El Secreto", "Un Secreto") > 0.7
        assert dedup.calculate_title_similarity("Amor", "Completamente Distinto") < 0.3

    def test_fuzzy_duplicate_detection(self):
        dedup = Deduplicator(fuzzy_threshold=0.85)
        dedup.register_title("El Secreto del Multimillonario")

        # Slight typo / variation
        is_dup, match, score = dedup.find_fuzzy_duplicate_title("El Secreto del Multimillonario!")
        assert is_dup is True
        assert match == "El Secreto del Multimillonario"
        assert score >= 0.85

        # Different title
        is_dup2, _, score2 = dedup.find_fuzzy_duplicate_title("La Heredera Rebelde")
        assert is_dup2 is False
        assert score2 < 0.85

    def test_deduplicate_series(self):
        dedup = Deduplicator()
        now = datetime.now(timezone.utc)
        series_items = [
            DiscoveredSeries(
                source_id="src1",
                source_url="https://demo.dramaapp.local/series/1",
                title="Drama One",
                extracted_at=now,
            ),
            DiscoveredSeries(
                source_id="src1",
                source_url="https://demo.dramaapp.local/series/2",
                title="Drama Two",
                extracted_at=now,
            ),
            DiscoveredSeries(
                source_id="src1",
                source_url="https://demo.dramaapp.local/series/1/",  # duplicate with trailing slash
                title="Drama One Duplicate",
                extracted_at=now,
            ),
        ]

        unique, duplicates = dedup.deduplicate_series(series_items)
        assert len(unique) == 2
        assert len(duplicates) == 1
        assert duplicates[0].title == "Drama One Duplicate"

    def test_deduplicate_episodes(self):
        dedup = Deduplicator()
        episodes = [
            DiscoveredEpisode(
                series_source_url="https://demo.dramaapp.local/series/1",
                season_number=1,
                episode_number=1,
                title="Episodio 1",
            ),
            DiscoveredEpisode(
                series_source_url="https://demo.dramaapp.local/series/1",
                season_number=1,
                episode_number=2,
                title="Episodio 2",
            ),
            DiscoveredEpisode(
                series_source_url="https://demo.dramaapp.local/series/1",
                season_number=1,
                episode_number=1,  # duplicate
                title="Episodio 1 Repetido",
            ),
        ]

        unique, duplicates = dedup.deduplicate_episodes(episodes)
        assert len(unique) == 2
        assert len(duplicates) == 1
        assert duplicates[0].title == "Episodio 1 Repetido"

    def test_reset(self):
        dedup = Deduplicator()
        dedup.mark_url_seen("https://example.com/test")
        assert dedup.is_url_seen("https://example.com/test") is True
        dedup.reset()
        assert dedup.is_url_seen("https://example.com/test") is False
