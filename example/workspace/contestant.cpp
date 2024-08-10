/**
 * Contestant's solution (example).
 *
 * @file example/workspace/contestant.cpp
 *
 * This file is supposed to be evaluated AGAINST the correct answer (i.e. the
 * judge). This example takes two numbers as input using the
 * @c cpdsa::buffer_scan function, then prints out their sum using the standard
 * C++ @c cout<< function.
 */

#include <iostream>

#include "lib/cpdsa/cpdsa.hpp"
using namespace std;

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cpdsa::buffer_scan(a, b);
    cout << a + b;
}