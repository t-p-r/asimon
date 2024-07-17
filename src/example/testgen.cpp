/**
 * @file src/example/testgen.cpp - Test generator (example).
 *
 * The output of this file is then taken as input for `judge.cpp` and
 * `contestant.cpp`. Arguments MUST be either `$number` or `rand $number1
 * $number2` where $number, $number1 and $number2 are integers. This example
 * prints out two randomly generated number (RNG) among all 32-bit integers.
 */

#include "lib/testlib-asimon/testlib.h"
using namespace std;

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    registerGen(argc, argv, 1);
    int lo = opt<int>("lo"), hi = opt<int>("hi");
    cout << rnd.next(lo, hi) << ' ' << rnd.next(lo, hi);
}
