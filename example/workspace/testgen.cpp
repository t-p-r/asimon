/**
 * Test generator (example).
 *
 * @file example/workspace/testgen.cpp
 *
 * The output of this file is then taken as input for @b judge.cpp and
 * @b contestant.cpp. Arguments MUST be "number1 number2" where
 * @a number1 and @a number2 are 32-bit signed integers. This example prints out
 * two randomly generated numbers (RNG) in the range [number1, number2]
 */

#include <chrono>
#include <iostream>
#include <random>
using namespace std;

mt19937 rng(chrono::high_resolution_clock::now().time_since_epoch().count());
int rand(int l, int r) { return uniform_int_distribution<int>(l, r)(rng); }

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    int lo = atoi(argv[1]), hi = atoi(argv[2]);
    cout << rand(lo, hi) << ' ' << rand(lo, hi);
}
