/**
 * src/base.cpp - Contestant's solution.
 *  
 * This file is supposed to be the correct answer.
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