"""Filesystem utilities."""

from pathlib import Path
from shutil import rmtree
import os


def get_dir(p: Path) -> Path:
    """Create a path regardless of its status and returns it."""
    p.mkdir(parents=True, exist_ok=True)
    return p


def delete_file(s: Path):
    "Silently deletes a file, suppressing any `OSError` raised."
    try:
        os.remove(s)
    except OSError:
        pass


def delete_folder(p: Path):
    "Silently deletes a folder, suppressing any `OSError` raised."
    try:
        rmtree(p)
    except OSError:
        pass
