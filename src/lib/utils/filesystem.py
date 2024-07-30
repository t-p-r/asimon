"""Filesystem utilities."""

from pathlib import Path
from shutil import rmtree
import os
from lib.utils import wrap_message, text_colors


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


def find_file_with_name(name: str, p: Path):
    """Find a file with name `name`.* in the directory `p`."""
    path, dirnames, filenames = list(p.walk())[0]  # we just care about p
    for filename in filenames:
        if (
            len(filename) > len(name)
            and filename.startswith(name)
            and filename[len(name)] == "."
        ):
            return filename
    raise Exception(
        wrap_message(
            "No source file corresponding with the name %s is found in the /workspace folder.",
            text_colors.RED,
        )
        % name
    )
