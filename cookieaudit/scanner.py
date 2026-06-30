"""Website cookie and third-party tracker scanner."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlparse

# Known analytics/ad domains (non-exhaustive, practical subset)
TRACKERS = {
    "google-analytics.com",
    "googletagmanager.com",
    "doubleclick.net",
    "facebook.net",
    "facebook.com/tr",
    "hotjar.com",
    "clarity.ms",
    "segment.io",
    "mixpanel.com",
    "amplitude.com",
}

CONSENT_HINTS = re.compile(
    r"cookie|consent|gdpr|rgpd|dsgvo|privacy|datenschutz|accept.*all",
    re.IGNORECASE,
)


@dataclass
class ScanResult:
    url: str
    status_code: int
    cookies: list[str] = field(default_factory=list)
    third_party_domains: list[str] = field(default_factory=list)
    trackers_found: list[str] = field(default_factory=list)
    has_consent_hints: bool = False
    issues: list[str] = field(default_factory=list)
    error: str | None = None


def scan_url(url: str, timeout: int = 15) -> ScanResult:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    result = ScanResult(url=url, status_code=0)

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CookieAudit/1.0 (+https://github.com/stefanSmk/cookieaudit)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result.status_code = resp.status
            headers = {k.lower(): v for k, v in resp.headers.items()}
            body = resp.read(500_000).decode("utf-8", errors="replace")

        result.cookies = _parse_cookies(headers)
        result.third_party_domains = _find_third_party(url, body)
        result.trackers_found = [d for d in result.third_party_domains if _is_tracker(d)]
        result.has_consent_hints = bool(CONSENT_HINTS.search(body))
        result.issues = _build_issues(result)
    except urllib.error.HTTPError as e:
        result.status_code = e.code
        result.error = str(e)
    except Exception as e:
        result.error = str(e)

    return result


def _parse_cookies(headers: dict[str, str]) -> list[str]:
    raw = headers.get("set-cookie", "")
    if not raw:
        return []
    # Multiple Set-Cookie often joined — split roughly by cookie names
    names = []
    for part in raw.split(","):
        name = part.split("=")[0].strip()
        if name and name not in names:
            names.append(name)
    return names


def _find_third_party(base_url: str, html: str) -> list[str]:
    host = urlparse(base_url).netloc.lower().removeprefix("www.")
    found: set[str] = set()

    for match in re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\s]+)', html, re.I):
        domain = urlparse(match).netloc.lower().removeprefix("www.")
        if domain and domain != host and not domain.endswith("." + host):
            found.add(domain)

    return sorted(found)


def _is_tracker(domain: str) -> bool:
    return any(t in domain for t in TRACKERS)


def _build_issues(result: ScanResult) -> list[str]:
    issues: list[str] = []
    if result.cookies and not result.has_consent_hints:
        issues.append("cookies_set_without_visible_consent_hints")
    if result.trackers_found:
        issues.append("third_party_trackers_detected")
    if any("google-analytics" in t or "googletagmanager" in t for t in result.trackers_found):
        issues.append("google_analytics_detected_cnil_risk")
    return issues
