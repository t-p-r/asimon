/**
 * src/base.cpp - Test generator.
 *
 * Arguments MUST be either `$number` or `rand $number1 $number2` where $number,
 * $number1 and $number2 are integers
 */

#include <bits/stdc++.h>
#include "base.cpp"
#include "lib/cpp/cpdsa/cpdsa.hpp"
#include "lib/cpp/cpdsa/cpdsa_experimental.hpp"
using namespace std;

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    int lo = INT_MIN, hi = INT_MAX;
    cout << rand(lo, hi) << ' ' << rand(lo, hi) << '\n';
}
