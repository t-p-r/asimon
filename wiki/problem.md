## How a created problem looks

Important: the arguments referred to below are from the file `config_create_problem.py`. Consider reading the documentation for that file (in `/examples/config`) first.

Consider a problem named `abc` with 50 tests (and `testdir_format` being `"test%C"`). After generating it using `create_problem.py`, this problem can be found in the `src/problem` folder. Its directory tree looks like this:

```
src
└── problem
	└──	abc
	 	├── test1			(optional)
	 	|	├── abc.inp
		|	└── abc.out
		├── ...
		├──	test50			(optional)
	    |
		├── abc.zip			(optional)
		├──	script.json
		|
		└── resources
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

From now on, we will refer to the folders `test1`, `test2`, ..., `test50` as the *test case folders*.

Details about subfolders:
- `script.json` contains information about the subtasks and the scripts used to create them.
- If `make_test_folders` is `True` then the *test case folders* will be created. 
- If `make_zip` is `True` then the file `abc.zip` will be created. This file normally only contains *test case folders*, except if `bundle_source` is `True`, in which case it will also contains `script.json` and the `resources` folder.
- If either option above is `False` then `script.json` will be created anyway.
- The `resources/misc` folder contains any file which is neither a test generator, a solution, or a checker, but is found in the `workspace` folder anyway.