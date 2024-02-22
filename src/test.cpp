#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;
using ii = pair<int, int>;

mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());

template <typename _t>
_t rand(_t l, _t r) {
    return uniform_int_distribution<_t>(l, r)(rng);
}

template <typename _t>
_t randf(_t l, _t r) {
    return uniform_real_distribution<_t>(l, r)(rng);
}

int seed(int r) {
    return uniform_int_distribution<int>(1, r)(rng);
}

// option 1: number
// option 2: rand number1 number2

int32_t main(int argc, char* argv[]) {
    cin.tie(0)->sync_with_stdio(0);
#ifdef _TPR_
    freopen("./dump/input_dump.txt", "w", stdout);
#endif

    int a = rand(0, (int)1e9), b = rand(0, (int)1e9);
    cout << a << ' ' << b << endl;
    cpdsa::median_heap<int> mh;
}
