## A created problem.

Consider a problem named `abc`. After generating it using `create_problem.py`, this problem can be found in the `src/problems` folder. Its directory looks like this:
```
src
└── problems
	└──	abc
		├── tests
		|	├──	script.json
		|	├── abc 		(optional)
		|	└── abc.zip 	(optional)
		├──	testgens
		|	├──	testgen.cpp
		|	├── testgen-for-a-special-case.cpp
		|	└──	...
		├──	solutions
		|	├── main-correct-solution.cpp
		|	└── other_solutions
		|		├── another-correct-solution.cpp
		|		├──	20-points.cpp
		|		├──	50-points.cpp
		|		└──	...
		|	... and any other files found in the "workspace" folder upon problem creation, for example:
		├──	statement.md (optional)
		└──	solution.md (optional)
```

The `abc` folder inside the `tests` folder contains all generated tests in text format. In DMOJ/VNOJ style, it looks like this:

```
abc
├── test1 
|	├── abc.inp
|	└── abc.out
├── test2
└──	...
```

If the `bundle_source` option in the configuration for `create_problem.py` is true, this folder (and the corresponding `.zip` file) will also contains:
- the `testgen` and `solution` folders
- every other files originally in the workspace; for example `statement.md` and `solution.md` in the tree above.