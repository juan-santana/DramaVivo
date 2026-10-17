"""Tests for SecurityManager, URL validation, and Allowlisting."""

import time
import pytest
from src.core.security import (
    DisallowedDomainError,
    InvalidURLError,
    SecurityManager,
)


class TestSecurityManager:
    """Test URL safety, domain allowlist, and rate limiting."""

    def test_domain_allowlist_matches(self):
        sec = SecurityManager(allowed_domains=["dramaapp.local", "example.com"])

        # Exact matches
        assert sec.is_domain_allowed("https://dramaapp.local/series") is True
        assert sec.is_domain_allowed("http://example.com") is True

        # Subdomain matches
        assert sec.is_domain_allowed("https://cdn.dramaapp.local/video") is True
        assert sec.is_domain_allowed("https://api.v2.example.com/shows") is True

        # Disallowed domains
        assert sec.is_domain_allowed("https://piratedramas.com") is False
        assert sec.is_domain_allowed("https://notdramaapp.local") is False

    def test_validate_valid_urls(self):
        sec = SecurityManager(allowed_domains=["example.com", "dramaapp.local"])
        url = "https://example.com/drama/123?page=1"
        assert sec.validate_url(url) == url

    def test_invalid_schemes_rejected(self):
        sec = SecurityManager(allowed_domains=["example.com"])

        with pytest.raises(InvalidURLError, match="Only http and https"):
            sec.validate_url("file:///etc/passwd")

        with pytest.raises(InvalidURLError, match="Only http and https"):
            sec.validate_url("ftp://example.com/file.txt")

        with pytest.raises(InvalidURLError, match="Only http and https"):
            sec.validate_url("javascript:alert(1)")

    def test_disallowed_domain_raises(self):
        sec = SecurityManager(allowed_domains=["allowed.com"])

        with pytest.raises(DisallowedDomainError):
            sec.validate_url("https://malicious.org/payload")

    def test_private_ip_addresses_blocked(self):
        sec = SecurityManager(allowed_domains=["*"])  # Even if star/wildcard conceptually

        # Loopback
        with pytest.raises(InvalidURLError, match="private/local/reserved"):
            sec.validate_url("http://127.0.0.1:8000/secret")

        # RFC1918 Class A
        with pytest.raises(InvalidURLError, match="private/local/reserved"):
            sec.validate_url("http://10.0.0.5/api")

        # RFC1918 Class C
        with pytest.raises(InvalidURLError, match="private/local/reserved"):
            sec.validate_url("http://192.168.1.1/router")

        # Link-local cloud metadata
        with pytest.raises(InvalidURLError, match="private/local/reserved"):
            sec.validate_url("http://169.254.169.254/latest/meta-data")

        # Localhost string
        with pytest.raises(InvalidURLError, match="localhost is prohibited"):
            sec.validate_url("http://localhost:3000/admin")

    def test_robots_txt_checking(self):
        sec = SecurityManager(allowed_domains=["example.com"], enforce_robots_txt=True)
        robots_content = """
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /series/
"""
        sec.set_robots_txt_content("https://example.com", robots_content)

        # Disallowed
        assert sec.can_fetch("https://example.com/admin/settings") is False
        assert sec.can_fetch("https://example.com/private/data") is False

        # Allowed
        assert sec.can_fetch("https://example.com/series/drama-1") is True
        assert sec.can_fetch("https://example.com/public/catalog") is True

    @pytest.mark.asyncio
    async def test_rate_limiter_pauses(self):
        sec = SecurityManager(allowed_domains=["example.com"], default_rate_limit_delay=0.1)

        start = time.monotonic()
        await sec.acquire_rate_limit("https://example.com/1")
        await sec.acquire_rate_limit("https://example.com/2")
        elapsed = time.monotonic() - start

        # Should have waited at least ~0.08s
        assert elapsed >= 0.08
