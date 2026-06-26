#!/usr/bin/env python3
"""
copilot_test.py

Simplified script: print system uptime using psutil only.

Usage: python3 copilot_test.py
"""

from __future__ import annotations
import time
import sys

try:
    import psutil
except ImportError:
    sys.stderr.write("psutil is required. Install with: pip install psutil\n")
    raise SystemExit(2)


def main() -> int:
    boot = psutil.boot_time()
    secs = time.time() - boot
    secs_int = int(secs)
    days, rem = divmod(secs_int, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")

    pretty = " ".join(parts)
    print(f"Uptime: {pretty} ({secs_int} seconds)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
