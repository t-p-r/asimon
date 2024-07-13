"""Various miscellanous helpers for asimon"""

import os
import shutil
from io import *
from pathlib import Path
from lib.text_colors import text_colors


def get_dir(p: Path) -> Path:
    """Create a path if it doesn't exist and returns it."""
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
        shutil.rmtree(p)
    except OSError:
        pass


def wrap_message(content: str, color: text_colors) -> str:
    """Wraps `color` around `content`. Only works for supported terminals. See `text_colors` for some examples."""
    return color + content + text_colors.END_COLOR


def send_message(content: str, color: text_colors, end="\n"):
    """Print to the terminal a message with colors and/or other attributes. See `text_colors` for some examples."""
    print(wrap_message(content, color), end=end)


def script_split(script: str) -> tuple[str, list]:
    """Split an execution script into the executable (first token) and its arguments (the other tokens).."""
    tokens = script.split()
    return (tokens[0], tokens[1:])


def write_prefix(ostream: TextIOWrapper, content: str, limit: int, end: str) -> None:
    """
    Write at most `limit` first characters of `content` to `ostream`.
    If `content` is longer than that then also write `...`.
    """
    if len(content) <= limit:
        ostream.write(content)
    else:
        ostream.write(content[: (limit + 1)])
        ostream.write(" ...")
    ostream.write(end)
