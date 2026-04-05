#!/usr/bin/env python3
"""pathwatch -- watch directories and run commands on file changes."""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import time

try:
    import watchdog
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False


def _poll_watch(paths: list[str], interval: float = 0.5) -> None:
    """Simple polling watcher -- no dependencies."""
    mtimes: dict[str, float] = {}
    for p in paths:
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    mtimes[fp] = os.path.getmtime(fp)
                except OSError:
                    pass
    print(f"Watching {len(mtimes)} files (Ctrl+C to stop)...")

    changed: set[str] = set()
    try:
        while True:
            for fp in list(mtimes):
                if not os.path.exists(fp):
                    del mtimes[fp]
                    continue
                try:
                    mtime = os.path.getmtime(fp)
                except OSError:
                    continue
                if mtime != mtimes[fp]:
                    changed.add(fp)
                    mtimes[fp] = mtime
            if changed:
                print(f"Changed: {', '.join(sorted(changed)[:5])}")
                changed.clear()
            # Check new files
            for p in paths:
                for root, dirs, files in os.walk(p):
                    for f in files:
                        fp = os.path.join(root, f)
                        if fp not in mtimes:
                            mtimes[fp] = os.path.getmtime(fp)
                            print(f"New: {fp}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def _watchdog_watch(paths: list[str], cmd: list[str] | None = None) -> None:
    """Use watchdog library if available."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            rel = os.path.relpath(event.src_path)
            prefix = "Modified"
            if event.event_type == "created":
                prefix = "Created"
            elif event.event_type == "deleted":
                prefix = "Deleted"
            elif event.event_type == "moved":
                prefix = "Moved"
            print(f"{prefix}: {rel}")
            if cmd:
                subprocess.run(cmd, shell=isinstance(cmd, str))

    observer = Observer()
    for p in paths:
        observer.schedule(Handler(), p, recursive=True)
    observer.start()
    try:
        print("Watching (Ctrl+C to stop)...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("\nStopped.")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print('Usage:')
        print('  python -m pathwatch path/to/dir')
        print('  python -m pathwatch path/to/dir --run "echo changed"')
        return
    paths = []
    cmd: list[str] | None = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--run':
            cmd = sys.argv[i+1:i+2]
            i += 2
        else:
            paths.append(sys.argv[i])
            i += 1

    if HAS_WATCHDOG:
        _watchdog_watch(paths, cmd)
    else:
        _poll_watch(paths)
        if cmd:
            print("--run flag requires watchdog library: pip install watchdog")


if __name__ == '__main__':
    main()
