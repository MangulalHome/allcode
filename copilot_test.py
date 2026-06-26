#!/usr/bin/env python3
"""
copilot_test.py

Print system uptime in a human-readable format.
Tries the following methods in order:
 - psutil.boot_time() if psutil is installed
 - /proc/uptime on Linux
 - Windows GetTickCount64 via ctypes
 - `uptime -s` or `uptime` command as a fallback

Usage: python3 copilot_test.py
"""

from __future__ import annotations
import os
import platform
import subprocess
import sys
import time


def seconds_to_human(seconds: float) -> str:
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days} day" + ("s" if days != 1 else ""))
    if hours:
        parts.append(f"{hours} hour" + ("s" if hours != 1 else ""))
    if minutes:
        parts.append(f"{minutes} minute" + ("s" if minutes != 1 else ""))
    if seconds or not parts:
        parts.append(f"{seconds} second" + ("s" if seconds != 1 else ""))
    return ", ".join(parts)


def uptime_seconds() -> float:
    # 1) psutil if available
    try:
        import psutil

        boot = psutil.boot_time()
        return time.time() - boot
    except Exception:
        pass

    # 2) Linux: /proc/uptime
    if os.path.exists("/proc/uptime"):
        try:
            with open("/proc/uptime", "r") as f:
                contents = f.read().split()
                return float(contents[0])
        except Exception:
            pass

    # 3) Windows: GetTickCount64 (milliseconds since boot)
    if platform.system() == "Windows":
        try:
            import ctypes

            GetTickCount64 = ctypes.windll.kernel32.GetTickCount64
            GetTickCount64.restype = ctypes.c_ulonglong
            ms = GetTickCount64()
            return float(ms) / 1000.0
        except Exception:
            # older Windows might not have GetTickCount64; try GetTickCount
            try:
                GetTickCount = ctypes.windll.kernel32.GetTickCount
                GetTickCount.restype = ctypes.c_uint32
                ms = GetTickCount()
                return float(ms) / 1000.0
            except Exception:
                pass

    # 4) Try `uptime -s` (start time) or `uptime -p` (pretty) or fallback to `uptime` output
    for cmd in (["uptime", "-s"], ["uptime", "-p"], ["uptime"]):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, universal_newlines=True)
            out = out.strip()
            # if uptime -s: parse start time
            if cmd == ["uptime", "-s"]:
                # Try parse ISO-like or locale datetime string
                try:
                    boot_time = time.mktime(time.strptime(out, "%Y-%m-%d %H:%M:%S"))
                    return time.time() - boot_time
                except Exception:
                    # try a more permissive parse by letting python parse common formats
                    try:
                        from datetime import datetime

                        dt = datetime.fromisoformat(out)
                        return time.time() - dt.timestamp()
                    except Exception:
                        pass
            # if uptime -p: output already pretty, but we can't get seconds reliably; print the text instead
            if cmd == ["uptime", "-p"] or cmd == ["uptime"]:
                # Return None-like sentinel by raising to be handled by caller
                raise RuntimeError(out)
        except subprocess.CalledProcessError:
            continue
        except FileNotFoundError:
            break
        except RuntimeError as e:
            # Propagate the pretty output via exception message
            raise
        except Exception:
            continue

    raise RuntimeError("Could not determine uptime on this system")


def main() -> int:
    try:
        secs = uptime_seconds()
        # if uptime_seconds raised RuntimeError with pretty output, handle that
    except RuntimeError as e:
        msg = str(e)
        # If the runtime error came with an `uptime -p` or `uptime` message, just print it
        if msg:
            print(msg)
            return 0
        print("Unable to determine uptime.")
        return 1

    if secs is None:
        print("Unable to determine uptime.")
        return 1

    human = seconds_to_human(secs)
    print(f"Uptime: {human} ({int(secs)} seconds)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
