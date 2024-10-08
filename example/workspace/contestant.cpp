/**
 * Contestant's solution (example).
 *
 * @file example/workspace/contestant.cpp
 *
 * This file is supposed to be evaluated AGAINST the correct answer (i.e. the
 * judge). This example takes two numbers as input using the
 * @c cpdsa::buffer_scan function, then prints out their sum using the standard
 * C++ @c cout<< function.
 *
 * The answer has a small chance to be incorrect. Can you spot it?
 */

#include <iostream>

#include "lib/cpdsa/cpdsa.hpp"
using namespace std;

int main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cpdsa::buffer_scan(a, b);
    if (b % 100 == 0) b--;
    cout << a + b;
}