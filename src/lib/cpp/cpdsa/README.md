# CPDSA - Data Structures and Algorithms for Competitive Programming

A C++ library containing well-known data structures and algorithms not found in the C++ STL. Aims to be fast, readable, modular and extensible.

This library is a translation of [my personal archive](https://github.com/t-p-r/CS_archive) to standards found in most C++ source codes.

## Prerequisites

- A C++ compiler (preferably GNU GCC 9.2.0+) set to compile in C++14 or newer (for example, by invoking the ```-std=c++17``` option).

## Uses

After cloning the repository, you may want to precompile the master header ```cpdsa.hpp```. Do note that all compilation options (for example ```-O2```, ```-DONLINE_JUDGE``` or ```-pipe```) must stay the same the header and the final program is compiled, else the precompiled header will most likely not be used.

For general users, simply ```#include<cpdsa.hpp>```.

For competitive programmers:
- all headers in the ```containers``` directory are independent and therefore copy-pasteable.

## Reliability

All headers has been tested with problems found on online judges. In the future, a seperate repository containing the testing process will be posted.

## Styles

A very simple coding style is used, without any macro or aliases (which is common with most competitive programmers).

Line width is at most 80 characters. Indentation is done using four spaces (and not ```Tab```).

The full ```clang-format``` style is:

```js
{ BasedOnStyle: Chromium, UseTab: Never, IndentWidth: 4, AllowShortIfStatementsOnASingleLine: true, ColumnLimit: 80 }
```

## Content

1. Containers (standalone data structures):
   - ```median_heap``` - a container maintaining its median.
   - ```ordered_set``` - dynamic segment tree to manage discrete elements.
   - ```bigint``` - arbitrary-precision arithmetic (in progress).
2. Graph (entire section in progress):
   - ```graph``` - graph representation (in progress).
   - ```tree``` - tree representation, child class of ```class``` (in progress).
   - ```weighted_graph``` and ```weighted_tree``` - weighted variants of the structures described above.
   - ```graph_algorithms``` - implements most popular algorithms on graphs (i.e. Dijkstra's).
   - ```tree_algorithms``` - implements most popular algorithms on trees (i.e. Kruskal's).
