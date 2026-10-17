"""Deduplication logic for discovered drama series and episodes."""

import difflib
import re
import unicodedata
from typing import Any
from pydantic import HttpUrl

from src.models.episode import DiscoveredEpisode
from src.models.series import DiscoveredSeries


def normalize_title(title: str) -> str:
    """
    Normalize drama title for comparison:
    - Unicode NFKD decomposition to strip accents/diacritics
    - Lowercase conversion
    - Strip punctuation and symbols
    - Collapse contiguous whitespace
    """
    if not title:
        return ""
    # Normalize unicode (e.g., 'Amor Secreto' -> 'Amor Secreto', accents removed)
    nfkd = unicodedata.normalize("NFKD", title)
    without_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Replace punctuation and special characters with single space
    clean = re.sub(r"[^\w\s]", " ", without_accents.lower())
    # Collapse multiple whitespaces
    return " ".join(clean.split())


class Deduplicator:
    """Tracks seen URLs and fuzzy titles to prevent duplicate processing."""

    def __init__(self, fuzzy_threshold: float = 0.88):
        self.fuzzy_threshold = fuzzy_threshold
        self._seen_urls: set[str] = set()
        self._seen_series_keys: set[str] = set()
        self._seen_episode_keys: set[tuple[str, int, int]] = set()
        self._seen_titles: dict[str, str] = {}  # normalized_title -> original_title

    def _url_to_str(self, url: str | HttpUrl) -> str:
        s = str(url).strip()
        # Normalize trailing slashes for URLs
        if s.endswith("/") and len(s) > 8:
            s = s[:-1]
        return s.lower()

    def is_url_seen(self, url: str | HttpUrl) -> bool:
        """Check if URL has already been recorded in the current session."""
        return self._url_to_str(url) in self._seen_urls

    def mark_url_seen(self, url: str | HttpUrl) -> bool:
        """
        Record URL as seen.
        Returns True if newly seen, False if it was already recorded.
        """
        url_str = self._url_to_str(url)
        if url_str in self._seen_urls:
            return False
        self._seen_urls.add(url_str)
        return True

    def calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Compute similarity ratio between two titles using normalized strings."""
        norm1 = normalize_title(title1)
        norm2 = normalize_title(title2)
        if not norm1 or not norm2:
            return 0.0
        if norm1 == norm2:
            return 1.0
        return difflib.SequenceMatcher(None, norm1, norm2).ratio()

    def find_fuzzy_duplicate_title(
        self, title: str, threshold: float | None = None
    ) -> tuple[bool, str | None, float]:
        """
        Check if a normalized title closely matches an already seen title.
        Returns: (is_duplicate, matched_original_title, similarity_score)
        """
        thresh = threshold if threshold is not None else self.fuzzy_threshold
        norm = normalize_title(title)
        if not norm:
            return False, None, 0.0

        if norm in self._seen_titles:
            return True, self._seen_titles[norm], 1.0

        best_match = None
        best_score = 0.0

        for seen_norm, orig_title in self._seen_titles.items():
            score = difflib.SequenceMatcher(None, norm, seen_norm).ratio()
            if score > best_score:
                best_score = score
                best_match = orig_title

        if best_score >= thresh and best_match:
            return True, best_match, best_score

        return False, None, best_score

    def register_title(self, title: str) -> None:
        """Register a title into the seen titles registry."""
        norm = normalize_title(title)
        if norm and norm not in self._seen_titles:
            self._seen_titles[norm] = title

    def deduplicate_series(
        self, series_list: list[DiscoveredSeries]
    ) -> tuple[list[DiscoveredSeries], list[DiscoveredSeries]]:
        """
        Filter out duplicates from a list of discovered series.
        Returns: (unique_series, duplicate_series)
        """
        unique: list[DiscoveredSeries] = []
        duplicates: list[DiscoveredSeries] = []

        for item in series_list:
            url_str = self._url_to_str(item.source_url)
            if url_str in self._seen_series_keys:
                duplicates.append(item)
                continue

            self._seen_series_keys.add(url_str)
            self.mark_url_seen(item.source_url)
            self.register_title(item.title)
            unique.append(item)

        return unique, duplicates

    def deduplicate_episodes(
        self, episodes_list: list[DiscoveredEpisode]
    ) -> tuple[list[DiscoveredEpisode], list[DiscoveredEpisode]]:
        """
        Filter out duplicate episodes based on (series_source_url, season_number, episode_number).
        Returns: (unique_episodes, duplicate_episodes)
        """
        unique: list[DiscoveredEpisode] = []
        duplicates: list[DiscoveredEpisode] = []

        for ep in episodes_list:
            key = (
                self._url_to_str(ep.series_source_url),
                ep.season_number,
                ep.episode_number,
            )
            if key in self._seen_episode_keys:
                duplicates.append(ep)
                continue

            self._seen_episode_keys.add(key)
            unique.append(ep)

        return unique, duplicates

    def reset(self) -> None:
        """Clear all tracking state for a new scrape session."""
        self._seen_urls.clear()
        self._seen_series_keys.clear()
        self._seen_episode_keys.clear()
        self._seen_titles.clear()
