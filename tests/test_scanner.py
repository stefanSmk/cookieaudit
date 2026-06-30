from cookieaudit.scanner import ScanResult, _build_issues, _find_third_party, _is_tracker


def test_scan_parses_third_party():
    html = '<script src="https://www.googletagmanager.com/gtm.js"></script>'
    domains = _find_third_party("https://example.com", html)
    assert any("googletagmanager" in d for d in domains)
    assert _is_tracker("www.googletagmanager.com")


def test_issues_when_cookies_and_no_consent():
    r = ScanResult(url="https://x.com", status_code=200, cookies=["session"], has_consent_hints=False)
    assert "cookies_set_without_visible_consent_hints" in _build_issues(r)
