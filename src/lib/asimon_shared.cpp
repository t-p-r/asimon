/**
 * src/lib/asimon_shared.cpp - Provides common functions for `contestant.cpp`,
 * `judge.cpp` and `testgen.cpp`. These includes:
 *  - a RNG with helper functions (to be moved into CPDSA when matured enough)
 *  - data parsing from argc and argv. The format is described in README.md
 */

#ifndef ASIMON_BASE
#define ASIMON_BASE

#include <chrono>
#include <concepts>
#include <random>
#include <vector>

namespace cpdsa {
// by default, uses the current time (the number of ms since 1970/1/1) as seed
std::mt19937_64 asimon_rng(
    std::chrono::high_resolution_clock::now().time_since_epoch().count());

/**
 * @brief Returns a random integral number in the range [l,r].
 * Conflicts with `stdlib.h`'s `rand()`.
 */
template <std::integral _Tp>
_Tp rand(_Tp l, _Tp r) {
    return std::uniform_int_distribution<_Tp>(l, r)(asimon_rng);
}

/**
 * @brief Returns a random integral number in the range [l,r].
 * Conflicts with `stdlib.h`'s `rand()`.
 */
template <std::floating_point _Tp>
_Tp randf(_Tp l, _Tp r) {
    return std::uniform_real_distribution<_Tp>(l, r)(asimon_rng);
}

/**
 * @brief Returns a random 32-bit integer in the range [1,r].
 */
int32_t seed(int32_t r) {
    return std::uniform_int_distribution<int32_t>(1, r)(asimon_rng);
}

/**
 * @brief Returns a random item from a non-empty vector.
 */
template <typename _Tp>
_Tp rand(const std::vector<_Tp>& v) {
    assert(v.size());
    return v[rand((size_t)0, v.size() - 1)];
}
}  // namespace cpdsa

int arg_count = 0;
std::vector<std::string> arg_vector;

/**
 * @brief Save the arguments.
 */
void register_arguments(int argc, char* argv[]) {
    for (int i = 0; i < argc; i++)
        arg_vector.emplace_back(std::string(argv[i]));
}

/**
 * @brief Set the RNG's seed to a specific value.
 * @param seed The RNG's new seed.
 */
template <std::integral _Tp>
void set_rng_seed(_Tp seed) {
    cpdsa::asimon_rng = std::mt19937_64(seed);
}

/**
 * @brief If the input token is parsed as `rand x y`, returns a random integer
 * in the range [x,y]; else return the parsed token as an integer.
 */
[[nodiscard]] int get_arg() {
    if (arg_vector[++arg_count][0] != 'r') return stoi(arg_vector[arg_count]);
    return arg_count += 2, cpdsa::rand(stoi(arg_vector[arg_count - 1]),
                                       stoi(arg_vector[arg_count]));
};

/**
 * @brief If the input token is parsed as `rand x y`, returns a random 64-bit
 * integer in the range [x,y]; else return the parsed token as a 64-bit integer.
 */
long long get_arg_ll() {
    if (arg_vector[++arg_count][0] != 'r') return stoll(arg_vector[arg_count]);
    return arg_count += 2, cpdsa::rand(stoll(arg_vector[arg_count - 1]),
                                       stoll(arg_vector[arg_count]));
};

/**
 * @brief If the input token is parsed as `rand x y`, returns a random `double`
 * in the range [x,y]; else return the parsed token as a `double`.
 */
double get_argd() {
    if (arg_vector[++arg_count][0] != 'r') return stof(arg_vector[arg_count]);
    return arg_count += 2, cpdsa::randf(stof(arg_vector[arg_count - 1]),
                                        stof(arg_vector[arg_count]));
};

#endif /* ASIMON_BASE */
