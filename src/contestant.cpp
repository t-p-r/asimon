#include <bits/stdc++.h>
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;

cpdsa::ordered_set<int, (int)-1e9, (int)1e9 + 1> st;

int32_t main() {
    cin.tie(0)->sync_with_stdio(0);
#ifdef _TPR_
    freopen("./dump/input_dump.txt", "r", stdin);
    freopen("./dump/output_dump.txt", "w", stdout);
#endif
    int t;
    while (cin >> t) {
        // cerr << t << '\n';
        if (t == 1) {
            int x;
            cin >> x;
            st.insert(x);
        } else if (t == 2) {
            int x;
            cin >> x;
            st.erase(x);
        } else if (t == 3) {
            if (st.empty())
                cout << "empty\n";
            else
                cout << st.find_by_order(1) << '\n';
        } else if (t == 4) {
            if (st.empty())
                cout << "empty\n";
            else
                cout << st.find_by_order(st.size()) << '\n';
        } else if (t == 5) {
            int x;
            cin >> x;
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
            cin >> x;
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
            cin >> x;
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
            cin >> x;
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