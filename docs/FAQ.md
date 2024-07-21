## Frequently asked questions:

(also a good place for beginners)


### **Q:** Why would I use it over Polygon?

**A:** ASIMON offers a subset of the [Polygon](https://polygon.codeforces.com/) problem preparation system. These are the reason you may want to use it:
- Local hosting.
- Very simple layout.
- Full control (and responsibility) over what you do.
- Multithread support (especially useful for problems with great time complexity, e.g. $O(n^3)$ where $n=420$).
- You are creating problems for anything other than Codeforces contests (if not, just use Polygon :)



### **Q:** What would a saved problem look like?

**A:** The problem can be found in the `src/problems` folder.
Consider a problem named `aplusb`, its directory looks like this:
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


### **Q:** Why are there no support for problem statement and solution? 

**A:** Because in most use cases you will write them (and host the problem) elsewhere. ASIMON cover most of your workflow except that; however, you can write your statement and solution in the `workspace` folder and the `create_problem.py` tool will bundle that, along with any miscellaneous files, into your saved problem folder anyway.