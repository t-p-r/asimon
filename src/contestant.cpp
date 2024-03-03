#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;

cpdsa::ordered_set<int> st;

mt19937_64 rng(1610612741);

// TODO: move these rands to CPDSA
template <typename _Tp>
_Tp rand(_Tp l, _Tp r) {
    return uniform_int_distribution<_Tp>(l, r)(rng);
}

template <typename _Tp>
_Tp randf(_Tp l, _Tp r) {
    return uniform_real_distribution<_Tp>(l, r)(rng);
}

int seed(int r) {
    return uniform_int_distribution<int>(1, r)(rng);
}

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
    int a, b;
    cpdsa::buffer_scan(a, b);
    cout << a + b;
}