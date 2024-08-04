/**
 * Test generator (example).
 *
 * @file docs/example/workspace/testgen.cpp
 *
 * The output of this file is then taken as input for @b judge.cpp and
 * @b contestant.cpp. Arguments MUST be "--lo number1 --hi number2" where
 * @a number1 and @a number2 are 32-bit signed integers. This example prints out
 * two randomly generated numbers (RNG) in the range [number1, number2]
 */

#include "lib/testlib-asimon/testlib.h"
using namespace std;

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    registerGen(argc, argv, 1);
    int lo = opt<int>("lo"), hi = opt<int>("hi");
    cout << rnd.next(lo, hi) << ' ' << rnd.next(lo, hi);
}
