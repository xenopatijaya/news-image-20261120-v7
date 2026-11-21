#!/usr/bin/env python3
"""Publish the pre-rendered entry image into the runner output folder."""

import os
import shutil
import sys
from pathlib import Path


def resolve_paths():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return source, target_dir / "entry.png"


def main():
    source, destination = resolve_paths()
    if not source.is_file():
        print(f"error: entry image not found at {source}", file=sys.stderr)
        return 1
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
