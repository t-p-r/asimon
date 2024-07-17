## ASIMON todos

Python side:
- Organize tests in Polygon format.

- migrate `list_generators()` elsewhere
- ~~migrate `os.system()` calls to `subprocess.run()` calls~~ (done)
    - ~~create helpers to pipe the testgen -> contestant / judge process~~
- ~~migrate RNG helpers to CPDSA~~ (done, now use testlib)
- support for unorthodox executable behaviour (TLE, MLE, etc)

- docs:
    - how to write custom checker in Python and checker in C++
- C++ error handling on Python side
    - Fix desync in testgen.py

- Include time and memory (maybe some other analysis module) in result() (and merge compare_*.py tools)


C++ side:
- ~~Support for arg identifier (e.g. `--vertex_count` / `-vC`, `--maxn` etc).~~ (done, now use testlib)
    - ~~Allow tests to be reproducible (e.g. by saving its seed in a metadata file)~~

- ~~"testlib.h" compatilibity~~ Customize `testlib` to bypass multiple file input.
- test folder name formatting?
- PROBLEM DATABASE (with unified problem format in a .json file)
- customize the linking the process (so that all `include` calls to libraries other than `testlib` or the C++ STL are rendered explicitly to the end .cpp file).