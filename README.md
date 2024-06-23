# ASIMON - Automated System for task Management and creatION

(no i'm not fixing that acronym)


## What is this?

A collection of tools to help you create, test and manage [competitive programming problems](cp_intro.md).

## Features:

- Test creation and packaging.
- Time and result comparision between implementations.

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

Open your prefered editor inside the `src` directory. Inside you will find three Python files:

- `vnoj_testgen.py`