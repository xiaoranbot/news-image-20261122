"""Entry point for make.fun news-image-20261122.

Copies the pre-rendered front page (entry.png, drawn by generate.py in
this repository) to the harness output directory. Standard library only,
no network, fully deterministic: the same bytes every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Outputs must be readable by the user that collects them.
    os.chmod(dst, 0o644)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
