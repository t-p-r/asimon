/**
 * @file src/example/testgen.cpp - Test generator (example).
 *
 * The output of this file is then taken as input for `judge.cpp` and
 * `contestant.cpp`. Arguments MUST be either `$number` or `rand $number1
 * $number2` where $number, $number1 and $number2 are integers. This example
 * prints out two randomly generated number (RNG) among all 32-bit integers.
 */

#include <bits/stdc++.h>
#include "lib/shared.cpp"
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    register_arguments(argc, argv); // this enables the retrieval of args
    int lo = INT_MIN, hi = INT_MAX;
    cout << cpdsa::rand(lo, hi) << ' ' << cpdsa::rand(lo, hi) << '\n';
}
