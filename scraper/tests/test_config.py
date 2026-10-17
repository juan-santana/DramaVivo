"""Tests for application configuration."""

from src.config import Settings, get_settings


class TestSettings:
    """Test Settings loading and validation."""

    def test_default_settings(self):
        settings = Settings()
        assert settings.schedule_hours >= 1
        assert "example.com" in settings.allowed_domains
        assert settings.output_dir == "output"

    def test_allowed_domains_string_parsing(self):
        settings = Settings(allowed_domains="alpha.com, beta.com , gamma.org")
        assert settings.allowed_domains == ["alpha.com", "beta.com", "gamma.org"]

    def test_allowed_domains_list_parsing(self):
        settings = Settings(allowed_domains=["Domain1.com ", "Domain2.com"])
        assert settings.allowed_domains == ["domain1.com", "domain2.com"]

    def test_get_settings_cached(self):
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
