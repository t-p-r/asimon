## ASIMON todos

- Organize tests in Polygon format.
- Support for arg identifier (e.g. `--vertex_count` / `-vC`, `--maxn` etc).
    - Allow tests to be reproducible (e.g. by saving its seed in a metadata file)
- migrate `list_generators()` elsewhere
- migrate `os.system()` calls to `subprocess.run()` calls
    - create helpers to pipe the testgen -> contestant / judge process
- migrate RNG helpers to CPDSA
- support for unorthodox executable behaviour (TLE, MLE, etc)

- docs:
    - how to write custom evaluator in Python and checker in C++
- C++ error handling on Python side