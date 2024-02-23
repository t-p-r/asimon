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
    // constexpr int lo = INT_MIN, hi = INT_MAX;
    constexpr int lo = (int)-1e9, hi = (int)1e9;
    // int sz = 0;
    // int n = 1e5;
    // while (n--) {
    //     int t = rand(1, 8);
    //     cout << t << ' ';
    //     if (t == 3 || t == 4) {
    //         cout << '\n';
    //     } else {
    //         int x = rand(lo, hi - 1);
    //         cout << x << '\n';
    //     }
    // }
    int a = rand(lo, hi), b = rand(lo, hi);
    cout << a << ' ' << b;
    // cerr<<(int)'r';return 0;
    // cpdsa::ordered_set<int, lo, hi> st;
    // st = cpdsa::ordered_set<int, lo, hi>();
    // return 0;
    // int num = 10000;
    // int cnt = 0;
    // while (clock() < (int)5e6) {
    //     st = cpdsa::ordered_set<int, lo, hi>();
    //     // cpdsa::ordered_set<int, lo, hi> st;
    //     for (int iter = 1; iter <= num; iter++)
    //         st.insert(rand(lo, hi - 1));
    //     cerr << (cnt += st.size()) << ' ' << st.find_by_order(5000) << '\n';
    //     // st.clear();
    // }
}
