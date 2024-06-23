/**
 * src/example/contestant.cpp - Contestant's solution (example).
 *
 * This file is supposed to be evaluated against the correct answer. This
 * example takes two numbers as input using the experimental
 * `cpdsa::buffer_scan` function, then prints out their (perhaps overflowed)
 * sum using the standard C++ `cout` function.
 */

#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
#include "lib/cpp/cpdsa/cpdsa_experimental.hpp"
using namespace std;

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cpdsa::buffer_scan(a, b);
    cout << a + b;
}