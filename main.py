#!/usr/bin/env python3
"""Copy the committed entry.png to $MAKEFUN_OUTPUT_DIR (default /output)."""
import os
import shutil
import sys


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print(f"Error: entry.png not found beside main.py (expected at {src}). "
              "Run `python3 draw.py` to generate it, or restore the committed entry.png.",
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"Copied {src} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
