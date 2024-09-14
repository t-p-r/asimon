# ASIMON - automated system for problem management and creation

(no i'm not fixing that acronym)


## What is this?

A *user-centric* platform written in Python and C++ to help you create and manage [competitive programming (CP) problems](/docs/cp_intro.md).

## Features

*Using your C++ source files*, ASIMON can:
- create multi-subtask test suites from your scripts.
- archive said tests in a format compatible to online judges (currently only DMOJ and its derivatives are supported).
- stress-test ~~and judge~~ your solutions, custom checker supported.
- store all these resources in a foolproof format.
  
### Other goodies:
- Multiprocessor support (especially useful for problems with great time complexity e.g. $O(n^3)$ where $n=420$).
- Compiled executable caching (basically if you change 1 of your 8 C++ source files then the other 7 won't be needlessly recompiled).
- Custom checker support via:
  - [testlib](https://github.com/MikeMirzayanov/testlib/) (as one of your C++ source files);
  - [the Python checker plugin system]().

## Requirement

A Linux or Windows-running machine with the following resources installed:
- Python 3.10+.
- Python package(s): `tabulate`. 
    - On Windows this can be installed using `pip install <package-name>`. On Arch-based Linux distros this can be done using `pacman -S python-<package-name>`. On any other platforms, good luck.
- A C++ compiler. Strongly recommend:
  - GNU GCC (basically everyone uses this)
  - Clang (its error messages are *much* more readable than GCC)

## Installation

1. Clone the repository.

```bash
$ git clone https://github.com/t-p-r/asimon
```

2. Go into the source directory.

```bash
$ cd asimon
```

3. (Optional, highly recommended) Initiate git submodules. 

```bash
$ git submodule update --init.
```

## Usage

See [the tutorial](/docs/tutorial.md).


## Frequently asked questions

### **Q:** Is this Polygon at home?

**A:** ASIMON offers a subset of the [Polygon](https://polygon.codeforces.com/) problem preparation system. Many features of the latter are not supported, including:
- a GUI
- support for validators
- support for writing statements and solutions
- and then some ...


However, there are reasons you may want to use ASIMON:
- Local hosting.
- Very gentle learning curve.
- Full control (and responsibility!) over what you do.
- Multiprocessor support.
- You are creating problems for anything other than Codeforces contests (if not, just use Polygon :)



### **Q:** What would a created problem look like?

**A:** See [this](https://github.com/t-p-r/asimon/wiki).


### **Q:** Why are there no support for problem statement and solution? 

**A:** Because in most use cases you will write them (and host the problem) elsewhere. ASIMON cover most of your workflow except that; however, you can write your statement and solution in the `workspace` folder and the `create_problem.py` tool will bundle that, along with any miscellaneous files, into your saved problem folder anyway.
