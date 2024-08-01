## How a created problem looks

Important: the arguments referred to below are from the file `config_create_problem.py`. Consider reading the documentation for that file (in `docs/examples/config`) first.

Consider a problem named `abc` with 50 tests (and `testdir_format` being `"test%T"`). After generating it using `create_problem.py`, this problem can be found in the `src/problem` folder. Its directory tree looks like this:

```
src
└── problem
	└──	abc
		├── test
		|	├── test1			(optional)
		|	|	├── abc.inp
		|	|	└── abc.out
		|	├── ...
		|	├──	test50			(optional)
		|   |
		|	├── abc.zip			(optional)
		|	└──	script.json
		|
		├──	testgen
		|	├──	testgen.cpp
		|	├── testgen-special-case.cpp
		|	└──	...
		|
		├──	solution
		|	├── main-correct-solution.cpp
		|	└── other_solutions
		|		├── another-correct-solution.cpp
		|		├──	partial-solution.cpp
		|		└──	...
		|
		├──	checker
		|	└──	checker.cpp
		|
		├──	misc
		|	├──	statement.md (optional)
		|	└──	solution.md (optional)
		|
		└── config_create_problem.py
```

Details about the subfolders:
- The `test` folder contains test data. `script.json` contains information about the subtasks and the scripts used to create them. If `make_test_folders` is `True` then the folders `test1`, `test2`, ..., `test50` will be created. If `make_zip` is `True` then the file `abc.zip` will be created. If either option is `False` then only `script.json` will be created.
	- `abc.zip` normally only contains the folders `test1`, `test2`, ..., `test50` and also `script.json`. If `bundle_source` is `True` however, this file will also includes every folder and file other than `test` in the `abc` directory (`testgen`, `solution`, ...).
- The `misc` folder contains any file which is neither a test generator, a solution, or a checker, but is found in the `workspace` folder anyway.