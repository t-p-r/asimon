# ASIMON - automated system for problem management and creation

(no i'm not fixing that acronym)


## What is this?

A set of tools (in Python) and libraries (in C++) to help you create and manage [competitive programming (CP) problems](cp_intro.md).

## Features:

- *Using your C++ source files*, ASIMON can:
    - create multi-subtask tests from your prompts *in an optionally reproducible manner*.
    - archive said tests in a format compatible to online judges (currently only DMOJ and its derivatives are supported).
    - stress-test and judge your implementations.
    - store all those resources in a foolproof format.
- *To help you write the C++ source files*, ASIMON includes these submodules:
    - an [version](https://github.com/t-p-r/testlib-asimon) of [testlib.h](https://github.com/MikeMirzayanov/testlib/) which completely bypasses file I/O.
    - [CPDSA](https://github.com/t-p-r/cpdsa) - a library containing many well-known data structures and algorithms but has yet to appear in the C++ STL.

## Requirement

A Linux or Windows-running machine with the following packages installed:
- `python`
- A C++ compiler, preferably `gcc` (`clang` may work but isn't tested). If you use CPDSA then the compiler must also supports C++20.

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
3. (Optional but highly recommended) Initiate git submodules. 

```bash
$ git submodule update --init.
```

## Usage

See [tutorial.md](/docs/tutorial.md).

## FAQ

See [FAQ.md](/docs/FAQ.md).