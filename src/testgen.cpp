#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
#include "lib/cpp/cpdsa/cpdsa_experimental.hpp"
using namespace std;
using ii = pair<int, int>;

mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

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

// option 1: number
// option 2: rand number1 number2

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
    int lo = INT_MIN, hi = INT_MAX;
    cout << rand(lo, hi) << ' ' << rand(lo, hi) << '\n';
}
