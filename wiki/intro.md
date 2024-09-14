# Introduction

This article serves as an introduction to some general knowledge about creating competitive programming (CP) problems, which is needed to use ASIMON. Those who have experience using Polygon or similar platforms can skip this.

Let us start with what is possibly the simplest problem in LeetCode:

> **Statement**: \
> Given two *integers* in the range $[-10^9,10^9]$, prints out their sum.
> 
> **Input**: \
> Two numbers $A$ and $B$ satisfying the constraints above.
> 
> **Output**: \
> $A+B$.
>
> **Sample Input**: \
> `1 2`
> 
> **Sample Output**: \
> `3`
>
> **Note**: $50$ percent of tests have the numbers in the range $[-10^4, 10^4]$.

Not much can be said about the solution, e.g. in C++:

```cpp
#include <iostream> // this method is older than your parents
// import std;      // C++20; no support from major compilers

int main() {        // or auto main() -> int
    int a, b;
    std::cin >> a >> b;
    std::cout << a + b;
}
```

From the side of those who creates these problem, however, some extras is needed, namely:
- test generators
- test validators
- custom checkers
- other solutions that are wittingly incorrect

## Test generators

The most common method of judging a solution is to iterate through *test cases* (i.e. feeding an input to the solution and see if its output matches that on the judge system).

For this problem, generating these *test cases* is rather simple: we can write down the two numbers and their sum by hand. However, this method is infeasible for most use cases, where:
- there can be as many as a few hundred test cases
- the inputs are large (e.g. around $10^6$ integers)

Thus there exists a need to automate this process using *test generators*. Here is an example for this problem:

```cpp
// gen.cpp

#include <chrono>
#include <iostream>
#include <random>

std::mt19937 rng(
    std::chrono::high_resolution_clock::now()
    .time_since_epoch()
    .count()
);

/**
 * Returns a random number in the range [l,r].
 * All numbers have equal chances to appear.
*/
int rand(int l, int r) {
    // return rand() % (r - l + 1) + l; // don't use this
    return std::uniform_int_distribution<int>(l, r)(rng);
}

int main() {
    int lo = -1e9, hi = 1e9;
    std::cout << rand(lo, hi) << ' ' << rand(lo, hi);
}
```

Some obscured parts:
- `std::mt19937` is a popular randomizing engine which is preferable to C's `rand()`. It needs a *seed* to initialize, which can be a constant, or in our application, a number that is practically random. For use with 64-bit numbers, use `std::mt19937_64`.
- `std::chrono::high_resulution_clock` is ... what you think it is.
- `now().time_since_epoch().count()` is the number of milliseconds elapsed since the Unix time *epoch* (12:00 AM, January 1, 1970) as measured by the clock.

Just run this program and we will receive two practically random numbers in $[-10^9,10^9]$. However, the original problem states that half the tests must have the two numbers in $[-10^4,10^4]$. Of course, we can just edit the variables `lo` and `hi`; however, there exists a more elegant solution to this problem: using *command line arguments*:

### Command line arguments

Normally programs are run with *arguments*. For example, consider the infamous command `rm -rf /`:
- `rm` is the name of the program
- `-rf` tells the program to **r**ecursively and **f**orcefully deletes everything in the specified directory `/`.

Programs in C and C++ have this ability (that includes `rm`!). The arguments are accessed through the constants `argc` and `argv` declared in the `main()` function:

```cpp
int main(int argc, char* argv[])
```

where:
- `argc` is the numbers of arguments;
- `argv` is an array of C strings containing the arguments.

So, for the command `rm -rf /`, we would have:
- `argc` = 3;
- `argv` = `{"rm", "-rf", "/"}`.

We can now use this ability to customize `lo` and `hi`:

```cpp
// gen.cpp

#include <chrono>
#include <iostream>
#include <random>
using namespace std; // don't use this outside of CP

mt19937 rng(
chrono::high_resolution_clock::now().time_since_epoch().count()
);

int rand(int l, int r) {
    return uniform_int_distribution<int>(l, r)(rng);
}

int main(int argc, char* argv[]) {
    // atoi() transforms a C string to an integer.
    int lo = atoi(argv[1]), hi = atoi(argv[2]);
    cout << rand(lo, hi) << ' ' << rand(lo, hi);
}
```

Now, we can just run the command `gen -10000 10000` to have `lo` = -10000 and `hi` = 10000. 


### Using testlib

[testlib.h]() is the de-facto official library for creating competitive programming problems. It is the prescribed method for writing test generators, validators and custom checkers. Here is a working example for this problem:

```cpp
// gen.cpp

#include "lib/testlib.h"

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    int lo = opt<int>("lo"), hi = opt<int>("hi");
    std::cout << rnd.next(lo, hi) << ' ' << rnd.next(lo, hi);
}
```

Some obscured parts:
- `registerGen()` initialize testlib in *test generator* mode. Without a `register*()` function, you won't be able to use the library.
- `opt` is testlib's method for accessing command line arguments. `opt<int>("lo")` will search for the string `"-lo"` or `"--lo"` in the argument list and return the next argument as an integer.
- `rnd` is testlib's in-house randomizing engine.

Now we can run, for example, the command `gen --lo -10000 --hi 10000` to get two randomized numbers in $[-10^4,10^4]$.

Further reading on [testlib's functionalities]() is strongly recommended.

## Test validators

This program *validates* whether the inputs generated by the test generator conforms to the specifications in the problem statement. ASIMON has yet to support this so we can skip through it.

## Custom checkers

A CP problem can have many acceptable output for one single input. In that case, just checking whether the solution's output matches that on the judge system is no longer enough, and a *custom checker* is needed.

ASIMON supports two types of a *custom checker*: a [Python plugin]() or a [standalone C++ program using testlib](). Here is an example for this problem:

```cpp
#include "lib/testlib.h"

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    int a = inf.readInt(), b = inf.readInt();
    int c = ans.readInt();  // judge system's answer
    if (c != a + b) {
        quitf(_fail, "Fatal error: judge's answer is incorrect: expected %d, found %d", a + b, c);
    }

    int d = ouf.readInt();  // solution's output
    if (d != c) {
        quitf(_wa, "Expected %d, found %d", c, d);
    }

    quitf(_ok, "ok");
}
```

## Incorrect solutions

These solutions are used to verify whether our test generators or custom checkers behaves properly. Here are a few ways a solution can go wrong for this problem:

### Wrong answer

```cpp
#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << a + b - 1;
}
```

### Exceeds time limit

```cpp
#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    std::cout << a + b - 1;
    while (true) a++;
}
```

### Runtime error

```cpp
#include <iostream>

int main() {
    vector<int> v(100);
    std::cout << v[200];

    int a, b;
    std::cin >> a >> b;
    std::cout << a + b;
}
```

## What now?

The programs above are essential for creating a CP problem. At least a test generator and a correct solution is required for any applications using ASIMON. At least one incorrect solution is needed for `stress.py`. 