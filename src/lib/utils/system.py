"""System utilities."""

from pathlib import Path
from shutil import rmtree
import os
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

    terminate_proc(
        f'Fatal error: No source file with name "{name}.cpp" or "{name}.c" '
        + "is found in the /workspace folder."
    )


def terminate_proc(message: str, returncode=1):
    """
    Sending `message` before terminate the process with `returncode`.
    If the process is a child of some parent process, the effect on
    the parent is undefined.
    """
    send_message(f"{message}\nAttempting termination...\n", text_colors.RED)
    exit(returncode)


def is_windows():
    try:
        import msvcrt

        del msvcrt
    except ModuleNotFoundError:
        return False
    else:
        return True
