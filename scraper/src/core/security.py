"""Security, domain allowlist, URL validation, and rate limiting."""

import asyncio
import ipaddress
import socket
import time
from typing import Sequence
import urllib.parse
import urllib.robotparser
import structlog

logger = structlog.get_logger(__name__)


class SecurityError(Exception):
    """Base exception for scraper security violations."""


class DisallowedDomainError(SecurityError):
    """Raised when an operation targets a domain not in the allowlist."""


class InvalidURLError(SecurityError):
    """Raised when a URL fails format, scheme, or safety checks."""


class RobotsDisallowedError(SecurityError):
    """Raised when a URL is blocked by robots.txt."""


class SecurityManager:
    """Manages domain allowlisting, URL sanitization, robots.txt, and rate limiting."""

    def __init__(
        self,
        allowed_domains: Sequence[str] | None = None,
        default_rate_limit_delay: float = 0.5,
        enforce_robots_txt: bool = True,
        resolve_dns_check: bool = False,
    ):
        """
        Initialize the security manager.

        :param allowed_domains: List of permitted domains or host suffixes.
        :param default_rate_limit_delay: Minimum seconds between requests to the same host.
        :param enforce_robots_txt: Whether to check robots.txt before allowing fetch.
        :param resolve_dns_check: Whether to perform DNS resolution to verify destination IP.
        """
        self.allowed_domains = [d.strip().lower() for d in (allowed_domains or []) if d.strip()]
        self.default_rate_limit_delay = default_rate_limit_delay
        self.enforce_robots_txt = enforce_robots_txt
        self.resolve_dns_check = resolve_dns_check

        # Per-domain rate limit timestamps
        self._last_request_times: dict[str, float] = {}
        self._rate_limit_locks: dict[str, asyncio.Lock] = {}

        # Cached robots.txt parsers
        self._robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}

    def is_domain_allowed(self, host_or_url: str) -> bool:
        """
        Check if the domain is in the allowlist.
        Supports exact match and subdomain suffixes (e.g. 'sub.example.com' matches 'example.com').
        """
        host = self.extract_host(host_or_url)
        if not host:
            return False

        if not self.allowed_domains:
            return False

        host = host.lower()
        for allowed in self.allowed_domains:
            allowed = allowed.lower()
            if host == allowed or host.endswith(f".{allowed}"):
                return True
        return False

    def validate_url(self, url: str) -> str:
        """
        Validate URL scheme, host safety, private IP ranges, and domain allowlist.

        Returns the validated canonical URL string.
        Raises InvalidURLError or DisallowedDomainError on failure.
        """
        if not url or not isinstance(url, str):
            raise InvalidURLError("URL must be a non-empty string")

        parsed = urllib.parse.urlparse(url.strip())

        # Scheme check
        if parsed.scheme.lower() not in ("http", "https"):
            raise InvalidURLError(
                f"Invalid or prohibited URL scheme: '{parsed.scheme}'. Only http and https are permitted."
            )

        # Host check
        host = (parsed.hostname or "").lower()
        if not host:
            raise InvalidURLError(f"URL missing hostname: '{url}'")

        # Disallow localhost / 127.0.0.1 by default unless explicitly allowed
        if host in ("localhost", "localhost.localdomain"):
            if not self.is_domain_allowed(host):
                raise InvalidURLError("Direct access to localhost is prohibited.")

        # Check for IP address literals
        try:
            ip_obj = ipaddress.ip_address(host)
            if (
                ip_obj.is_private
                or ip_obj.is_loopback
                or ip_obj.is_link_local
                or ip_obj.is_reserved
                or ip_obj.is_unspecified
            ):
                if not self.is_domain_allowed(host):
                    raise InvalidURLError(
                        f"Access to private/local/reserved IP address is prohibited: {host}"
                    )
        except ValueError:
            # host is a domain name, not an IP literal
            pass

        # Optional DNS resolution safety check
        if self.resolve_dns_check:
            try:
                addr_info = socket.getaddrinfo(host, None)
                for item in addr_info:
                    ip_str = item[4][0]
                    ip_obj = ipaddress.ip_address(ip_str)
                    if (
                        ip_obj.is_private
                        or ip_obj.is_loopback
                        or ip_obj.is_link_local
                        or ip_obj.is_reserved
                    ):
                        if not self.is_domain_allowed(host):
                            raise InvalidURLError(
                                f"Hostname '{host}' resolved to restricted private IP: {ip_str}"
                            )
            except socket.gaierror:
                pass

        # Allowlist check
        if not self.is_domain_allowed(host):
            raise DisallowedDomainError(
                f"Domain '{host}' is not present in allowed domains list: {self.allowed_domains}"
            )

        return url.strip()

    def extract_host(self, host_or_url: str) -> str:
        """Extract clean hostname from URL or raw host string."""
        if not host_or_url:
            return ""
        if "://" in host_or_url:
            parsed = urllib.parse.urlparse(host_or_url)
            return (parsed.hostname or "").lower()
        # Might be host:port or just host
        return host_or_url.split(":")[0].strip().lower()

    async def acquire_rate_limit(self, host_or_url: str, delay: float | None = None) -> None:
        """
        Enforce rate limit per host by pausing execution if called too quickly.
        """
        host = self.extract_host(host_or_url)
        if not host:
            return

        interval = delay if delay is not None else self.default_rate_limit_delay
        if interval <= 0:
            return

        if host not in self._rate_limit_locks:
            self._rate_limit_locks[host] = asyncio.Lock()

        async with self._rate_limit_locks[host]:
            now = time.monotonic()
            last_time = self._last_request_times.get(host, 0.0)
            elapsed = now - last_time
            if elapsed < interval:
                wait_time = interval - elapsed
                await asyncio.sleep(wait_time)
            self._last_request_times[host] = time.monotonic()

    def set_robots_txt_content(self, base_url: str, content: str) -> None:
        """Directly populate the robots.txt rules cache for a base URL."""
        host = self.extract_host(base_url)
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(content.splitlines())
        self._robots_cache[host] = parser

    def can_fetch(self, url: str, user_agent: str = "*") -> bool:
        """
        Check if robots.txt permits crawling the URL.
        If robots.txt has not been cached and robots enforcement is enabled, returns True by default.
        """
        if not self.enforce_robots_txt:
            return True

        host = self.extract_host(url)
        parser = self._robots_cache.get(host)
        if parser is None:
            # If no robots.txt loaded, default to allowing
            return True
        return parser.can_fetch(user_agent, url)
