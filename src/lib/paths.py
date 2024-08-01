from pathlib import Path

# Common paths in asimon:

rootdir = Path(__file__).parent.parent
# The project's root directory, .../asimon/src/
workspace = rootdir / "workspace"
# C++ workspace.
bindir = rootdir / "bin"
# Where the C++ executables are dumped into.
logdir = rootdir / "log"
# Log folder.
result_file_location = logdir / "result.txt"
# Reports on generic informations about the run.
universal_problems_dir = rootdir / "problem"
# Where we store problems.
cache_dir = rootdir / "cache"
# Store pair of .c/.cpp files and its binary. Enables skipping of repeated compilation.

