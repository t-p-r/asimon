#include <bits/stdc++.h>
#include "lib/asimon_shared.cpp"
#include "lib/cpp/cpdsa/cpdsa.hpp"
using namespace std;

#define int long long

const int mn = 1011;
const int EPS = 1e6, EPS_HIGH = 1e12;

int mindiv[EPS + 1];
vector<int> prime_list;

int a[mn];
int big_primes[] = {9263231,      4291843,      5525059,      9655777,
                    86771693,     59444653,     80967181,     79042427,
                    445183399,    218268641,    869948749,    888815089,
                    8334864943,   5196064429,   5842059071,   7522752521,
                    97594098323,  87383351249,  75061397809,  14009308153,
                    136138940929, 385752648289, 871704145199, 263336366333};

int32_t main(int argc, char* argv[]) {
    for (int i = 2; i * i <= EPS; i++)
        if (!mindiv[i])
            for (int j = i * i; j <= EPS; j += i)
                mindiv[j] = i;
    for (int i = 2; i <= EPS; i++)
        if (!mindiv[i]) prime_list.emplace_back(i);

    cin.tie(0)->sync_with_stdio(0);
    register_arguments(argc, argv);

    int n = get_arg(), lim = 1e18;
    cout << n << '\n';

    for (int i = 1; i <= n; i++)
        a[i] = 1;

    int saturation_step = get_arg();
    int saturation_count = get_arg();

    while (saturation_step--) {
        int p = big_primes[cpdsa::rand(0, 23)];
        for (int iter = 1; iter <= saturation_count; iter++) {
            int i = cpdsa::rand(1LL, n);
            if (a[i] <= lim / p) a[i] *= p;
        }
    }

    for (int i = 1; i <= n; i++)
        cout << a[i] << ' ';
}
