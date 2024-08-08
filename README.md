# ASIMON - automated system for problem management and creation

(no i'm not fixing that acronym)


## What is this?

A set of tools (in Python) and libraries (in C++) to help you create and manage [competitive programming (CP) problems](/docs/cp_intro.md).

## Features

- *Using your C++ source files*, ASIMON can:
    - create multi-subtask test suites from your scripts.
    - archive said tests in a format compatible to online judges (currently only DMOJ and its derivatives are supported).
    - stress-test ~~and judge~~ your solutions.
    - store all these resources in a foolproof format.
  
### Other goodies
- Parallel compilation and test execution (especially useful for problems with great time complexity e.g. $O(n^3)$ where $n=420$).
- ~~Custom checker support~~ (TBA)

## Requirement

A Linux or Windows-running machine with the following resources installed:
- Python 3.0+.
- Python package(s): `tabulate`. 
    - On Windows this can be installed using `pip install <package-name>`. On Arch-based Linux distros this can be done using `pacman -S python-<package-name>`. On any other platforms, refer to their documentations.
- A C++ compiler. GNU GCC and Clang are strongly recommended. If you use CPDSA then also enable support for C++20 or newer standards.


## Installation

1. Clone the repository.

```bash
$ git clone https://github.com/t-p-r/asimon
```

2. Go into the source directory

```bash
$ cd asimon
$ cd src
```

3. (Optional, highly recommended) Initiate git submodules. 

```bash
$ git submodule update --init.
```

## Usage

See [the tutorial](/docs/tutorial.md).

## FAQ

See [FAQ.md](/docs/FAQ.md).
