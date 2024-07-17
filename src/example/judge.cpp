/**
 * @file src/example/judge.cpp - Judge's solution (example).
 *
 * This file is supposed to be the correct answer. This
 * example takes two numbers as input, then prints out their (perhaps
 * overflowed) sum, using the standard C++ `cin`/`cout` functions.
 */

#include <iostream>
using namespace std;

int main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cin >> a >> b;
    cout << a + b;
}