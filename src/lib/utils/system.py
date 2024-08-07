"""System utilities."""

from pathlib import Path
from shutil import rmtree
from enum import Enum
import os
from lib.exceptions import RedException
from lib.utils.formatting import send_message, text_colors


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

    for ext in [".cpp", ".c"]:
        p = Path(p / f"{name}{ext}")
        if p.exists():
            return p

    terminate(
        f'No source file with name "{name}.cpp" or "{name}.c" is found in the /workspace folder.'
    )


def terminate(message: str):
    send_message(message, text_colors.RED)
    exit(0)


def is_windows():
    try:
        import msvcrt
        del msvcrt
    except ModuleNotFoundError:
        return False
    else:
        return True
