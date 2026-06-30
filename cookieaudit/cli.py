import argparse
import json
import sys

from .scanner import scan_url


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan a website for cookies, trackers, and privacy hints.",
    )
    parser.add_argument("url", help="URL to scan")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Issues only")
    args = parser.parse_args(argv)

    result = scan_url(args.url)

    if result.error and result.status_code == 0:
        print(f"Error: {result.error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            "url": result.url,
            "status_code": result.status_code,
            "cookies": result.cookies,
            "third_party_domains": result.third_party_domains,
            "trackers_found": result.trackers_found,
            "has_consent_hints": result.has_consent_hints,
            "issues": result.issues,
            "error": result.error,
        }, indent=2))
        return 0

    if not args.quiet:
        print(f"URL:      {result.url}")
        print(f"Status:   {result.status_code}")
        print(f"Cookies:  {', '.join(result.cookies) or 'none'}")
        print(f"Trackers: {', '.join(result.trackers_found) or 'none'}")
        print(f"Consent hints in HTML: {'yes' if result.has_consent_hints else 'no'}")
        print()

    if result.issues:
        print("Issues:")
        for issue in result.issues:
            print(f"  • {issue}")
    else:
        print("No obvious issues detected (heuristic scan only).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
