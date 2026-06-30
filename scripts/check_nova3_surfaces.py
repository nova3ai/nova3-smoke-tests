#!/usr/bin/env python3
"""Smoke-test Nova3 AI public authority surfaces."""

from __future__ import annotations

import sys
import urllib.request

URLS = [
    "https://nova3.ai/",
    "https://nova3.ai/sandbox",
    "https://nova3.ai/build",
    "https://nova3.ai/guide/ai-operations",
    "https://nova3.ai/surface",
    "https://nova3.ai/current-state",
    "https://nova3.ai/llms.txt",
]


def check(url: str) -> tuple[str, int, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "nova3-smoke-tests/1.0 (+https://nova3.ai)"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read(2048).decode("utf-8", errors="replace")
        return url, response.status, body


def main() -> int:
    failures: list[str] = []
    for url in URLS:
        try:
            checked_url, status, body = check(url)
        except Exception as exc:  # pragma: no cover - command-line diagnostic
            failures.append(f"{url} failed: {exc}")
            continue

        marker = "Nova3" if "Nova3" in body else "no Nova3 marker"
        print(f"{status} {checked_url} ({marker})")
        if status >= 400 or "Nova3" not in body:
            failures.append(f"{checked_url} returned {status} with {marker}")

    if failures:
        print("\nFailures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
