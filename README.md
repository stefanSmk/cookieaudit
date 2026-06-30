# CookieAudit

**Languages:** English · [Deutsch](./README.de.md) · [Français](./README.fr.md)

Self-hosted **website cookie and tracker scanner** for quick GDPR / CNIL sanity checks.

Before you launch a site or sign a DPA, you want to know: what cookies drop on first visit? Is Google Analytics loading before consent? Does the page mention cookies at all?

This is a **heuristic CLI tool** — not a replacement for a legal audit. It catches obvious red flags fast.

Complements [PrivaQuest](https://github.com/stefanSmk/privaquest) (handle requests) and [RopaDesk](https://github.com/stefanSmk/ropadesk) (document processing).

## Features

- Fetches URL, lists Set-Cookie headers
- Detects third-party script domains
- Flags known trackers (GA, GTM, Facebook, Hotjar, etc.)
- Checks HTML for consent/privacy keywords
- JSON output for CI pipelines
- Zero external dependencies (stdlib only)

## Install

```bash
git clone https://github.com/stefanSmk/cookieaudit.git
cd cookieaudit
pip install -e .
```

## Usage

```bash
cookieaudit https://example.com
cookieaudit https://example.com --json
cookieaudit https://example.com -q
```

Example output:

```
URL:      https://example.com
Status:   200
Cookies:  session_id
Trackers: www.googletagmanager.com
Consent hints in HTML: no

Issues:
  • cookies_set_without_visible_consent_hints
  • third_party_trackers_detected
  • google_analytics_detected_cnil_risk
```

## Use cases

| Who | Why |
|-----|-----|
| **DE** | DSGVO ePrivacy — cookies need consent |
| **FR** | CNIL enforcement on analytics |
| **EN** | Pre-launch checks for EU-facing sites |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Limits

- Single-page fetch only (no JavaScript execution)
- Keyword detection is rough — false positives/negatives happen
- Not legal advice

## Other languages

- **English** — this file (`README.md`)
- [Deutsch](./README.de.md)
- [Français](./README.fr.md)

## License

MIT
