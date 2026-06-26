#!/usr/bin/env python3
"""
extract_private_ips.py

Extracts private IPv4 addresses from input text (stdin or a file) in the
private ranges:
 - 10.0.0.0 - 10.255.255.255
 - 172.16.0.0 - 172.31.255.255
 - 192.168.0.0 - 192.168.255.255

Prints one IP per line in first-seen order, deduplicated.
"""
import re
import sys

PATTERN = re.compile(
    r"\b(?:(?:10\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\."
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d))|"
    r"(?:172\.(?:1[6-9]|2\d|3[01])\."
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d))|"
    r"(?:192\.168\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\."
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)))\b"
)


def extract_private_ips(text: str):
    seen = set()
    ordered = []
    for m in PATTERN.finditer(text):
        ip = m.group(0)
        if ip not in seen:
            seen.add(ip)
            ordered.append(ip)
    return ordered


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    for ip in extract_private_ips(text):
        print(ip)


if __name__ == "__main__":
    main()
