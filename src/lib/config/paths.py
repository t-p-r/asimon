"""Common paths in ASIMON."""

from pathlib import Path
from lib.utils.system import get_dir

rootdir = Path(__file__).parent.parent.parent
# The project's root directory, .../asimon/src/
workspace = rootdir / "workspace"
# C++ workspace.
bindir = get_dir(rootdir / "bin")
# Where the C++ executables are dumped into.
logdir = rootdir / "log"
# Log folder.
result_file_location = logdir / "result.txt"
# Reports on generic informations about the run.
problems_dir = rootdir / "problem"
# Where we store problems.
cache_dir = get_dir(rootdir / "cache")
# Store pair of .c/.cpp files and its binary. Enables skipping of repeated compilation.
