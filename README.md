# ASIMON - Automated System for task Management and creatION

(no i'm not fixing that acronym)


## What is this?

A collection of tools to help you create, test and manage [competitive programming problems](cp_intro.md).

## Features:

- Test creation and packaging.
- Time and result comparison between implementations.

Currently C++ is the only supported language.


## Requirement

A Linux-running machine with the following packages installed:
- `python`
- `zip`
- A C++ compiler supporting C++20, preferably `gcc` (`clang` may work but isn't tested).

## Getting started

1. Clone the repository.
2. (Optional but highly recommended) Initiate git submodules. Simply `cd` to the repo folder and `git submodule update --init`.

## Usage

Open your preferred editor inside the `src` directory.
Inside the `example` directory are the three default C++ files. Copy them to the `src` directory. 

Now you will find three Python files:

- `compare_result.py`
- `compare_time.py`
- `testgen.py`

They pretty much do what you expect them to do. Each file has a list of user variables that you are expected to edit (which is powerful enough that no GUI is needed) before running.