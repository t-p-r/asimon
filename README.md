# ASIMON - automated system for problem management and creation

(no i'm not fixing that acronym)


## What is this?

A set of tools (in Python) and libraries (in C++) to help you create and manage [competitive programming (CP) problems](cp_intro.md).

## Features

- *Using your C++ source files*, ASIMON can:
    - create multi-subtask test suites from your prompts.
    - archive said tests in a format compatible to online judges (currently only DMOJ and its derivatives are supported).
    - stress-test and judge your solutions.
    - store all those resources in a foolproof format.
- *To help you write the C++ source files*, ASIMON includes these submodules:
    - an [version](https://github.com/t-p-r/testlib-asimon) of [testlib.h](https://github.com/MikeMirzayanov/testlib/) which completely bypasses file I/O.
    - [CPDSA](https://github.com/t-p-r/cpdsa) - a library containing some data structures and algorithms not included in the C++ STL.
  
### Other goodies
- Multithreading (especially useful for problems with great time complexity e.g. $O(n^3)$ where $n=420$).

## Requirement

A Linux or Windows-running machine with the following resources installed:
- Python version 3.0+
  - `pip` package(s): `tabulate`.
- A C++ compiler. GNU GCC is strongly recommended. If you use CPDSA then the compiler must also supports C++20.


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