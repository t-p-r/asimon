#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;

cpdsa::ordered_set<int> st;

mt19937_64 rng(1610612741);

// TODO: move this rands to CPDSA
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

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
    int n = 1e5, lo = (int)-1e9, hi = (int)1e9 + 1;
    while (n--) {
        int t = rand(1, 8);
        if (t == 1) {
            int x;
            x = rand(lo, hi - 1);
            st.insert(x);
        } else if (t == 2) {
            int x;
            x = rand(lo, hi - 1);
            st.erase_once(x);
        } else if (t == 3) {
            if (st.empty()) {
                cout << "empty\n";
            } else {
                cout << st.find_by_order(1) << '\n';
            }
        } else if (t == 4) {
            if (st.empty()) {
                cout << "empty\n";
            } else {
                cout << st.find_by_order(st.size()) << '\n';
            }
        } else if (t == 5) {
            int x;
            x = rand(lo, hi - 1);
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.lower_bound(x + 1);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 6) {
            int x;
            x = rand(lo, hi - 1);
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.lower_bound(x);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 7) {
            int x;
            x = rand(lo, hi - 1);
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.upper_bound(x - 1);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        } else if (t == 8) {
            int x;
            x = rand(lo, hi - 1);
            if (st.empty()) {
                cout << "empty\n";
                continue;
            }
            auto result = st.upper_bound(x);
            if (result == 1000000001) {
                cout << "no\n";
            } else {
                cout << result << '\n';
            }
        }
    }
}