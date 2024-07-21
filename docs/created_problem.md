## A created problem.

Consider a problem named `aplusb`. After generating it using `create_problem.py`, this problem can be found in the `src/problems` folder. Its directory looks like this:
```
src
└── problems
	└──	aplusb
		├── tests
		|	├──	script.json
		|	├── aplusb 		(optional)
		|	└── aplusb.zip 	(optional)
		├──	testgen
		|	├──	testgen.cpp
		|	├── testgen-for-a-special-case.cpp
		|	└──	...
		├──	solution
		|	├── main-correct-solution.cpp
		|	└── contestant
		|		├── another-correct-solution.cpp
		|		├──	20-percent-solution.cpp
		|		├──	50-percent-solution.cpp
		|		└──	...
		|	... and any other files found in the "workspace" folder upon problem creation, for example:
		├──	statement.md (optional)
		└──	solution.md (optional)
```

The `aplusb` folder inside the `tests` folder contains all generated tests in text format. In VNOJ style, it looks like this:

```
aplusb
├── test1 
|	├── aplusb.inp
|	└── aplusb.out
├── test2
└──	...
```

If the `bundle_source` option in the configuration for `create_problem.py` is true, this folder (and the corresponding `.zip` file) will also have:
- the `testgen` and `solution` folders
- every other files originally in the workspace; for example `statement.md` and `solution.md` in the tree above.