## ASIMON todos

- Allow tests to be reproducible (e.g. by saving its seed in a metadata file)
- Organize tests in Polygon format.
- 
- Support for arg identifier (e.g. `--vertex_count` / `-vC`, `--maxn` etc).
- migrate `list_generators()` elsewhere
- migrate `os.system()` calls to `subprocess.run()` calls
    - create helpers to pipe the testgen -> contestant / judge process