## ASIMON todos

Python side:
- Organize tests in Polygon format.

- migrate `list_generators()` elsewhere
- migrate `os.system()` calls to `subprocess.run()` calls
    - create helpers to pipe the testgen -> contestant / judge process
- migrate RNG helpers to CPDSA
- support for unorthodox executable behaviour (TLE, MLE, etc)

- docs:
    - how to write custom checker in Python and checker in C++
- C++ error handling on Python side
    - Fix desync in testgen.py

- Include time and memory (maybe some other analysis module) in result() (and merge compare_*.py tools)


C++ side:
- Support for arg identifier (e.g. `--vertex_count` / `-vC`, `--maxn` etc).
    - Allow tests to be reproducible (e.g. by saving its seed in a metadata file)

- "testlib.h" compatilibity
- test folder name formatting?