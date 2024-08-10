/**
 * Judge's solution (example).
 *
 * @file example/workspace/judge.cpp
 *
 * This file is supposed to be the correct answer. This
 * example takes two numbers as input, then prints out their sum,
 * using the standard C++ @c cin>> / @c cout<< functions.
 */

#include <iostream>
using namespace std;

int main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cin >> a >> b;
    cout << a + b;
}