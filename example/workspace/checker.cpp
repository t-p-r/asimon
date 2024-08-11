/**
 * External checker using testlib.
 *
 * @file example/workspace/checker.cpp
 *
 */

#include "lib/testlib.h"

using namespace std;

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    int a = inf.readInt(), b = inf.readInt();

    int c = ans.readInt();  // correct sum
    if (c != a + b) {
        quitf(_fail, "Answer is not correct: expected %d, found %d", a + b, c);
    }

    int d = ouf.readInt();  // possibly incorrect sum
    if (d != c) {
        quitf(_wa, "Expected %d, found %d", c, d);
    }

    quitf(_ok, "ok");
}