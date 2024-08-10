/**
 * ASIMON: Compatibility layer for testlib.h.
 *
 * THIS FILE DOES NOT, IN ANY WAY, IMPLEMENTS EVEN A FUNCTIONAL SUBSET OF
 * TESTLIB.H, NOR INDUCE ANY CHANGES ON THE USER'S SIDE, BUT MERELY ADD A
 * COMPATIBILITY LAYER SO THAT THE ORIGINAL VERSION OF TESTLIB.H CAN WORK WITH
 * ASIMON'S FILELESS I/O POLICY.
 *
 * It is imperative that the original testlib repo be included in the folder
 * containing this file. Do this if you have not done so after installing
 * ASIMON:
 *
 *          $ git submodule update --init
 *
 * to initialize the submodules, including testlib.
 *
 * If you don't want to do so, head to this directory and directly clone testlib
 * from source:
 *
 *          $ git clone https://github.com/MikeMirzayanov/testlib/
 *
 * @file /src/workspace/lib/testlib.h
 */

#ifndef TESTLIB_ASIMON
#define TESTLIB_ASIMON

/* Overrides vanilla registerTestlibCmd */
#define registerTestlibCmd __registerTestlibCmd_deprecated
#include "testlib/testlib.h"
#undef registerTestlibCmd

#include <cassert>

static const size_t UUID_LENGTH = 36;
static const size_t _ASIMON_STR_RESERVE = 32 * 1024 * 1024;  // 32MB
char uuid1[UUID_LENGTH];
char uuid2[UUID_LENGTH];

std::string _asimon_input;
std::string _asimon_answer;
std::string _asimon_output;

/**
 * @brief Get the next byte from @c stdin, or return @a EOF if stdin
 * is empty.
 *
 * @note Use @c fread() to perform efficient bulk reading.
 */
uint8_t getc() noexcept {
    static const size_t BUFSIZE = 1 << 16;  // 64 KB
    static char buf[BUFSIZE];
    static size_t bufat = 0, bufend = 0;
    if (bufat == bufend) {
        bufend = fread(buf, sizeof(char), BUFSIZE, stdin);
        bufat = 0;
    }
    return bufend ? buf[bufat++] : EOF;
}

/**
 * @brief Consumes all of @c stdin into a string.
 */
inline void __asimon_getstdin_all(std::string& dest) {
    for (char c = getc(); c != EOF; c = getc()) dest.push_back(c);
}

/**
 * @brief Returns a string from the current @c stdin pointer, up to (but not
 * including) the first occurence of @c uuid.
 *
 * @param uuid The UUID pattern to match.
 *
 * @note After this function is done, the @c stdin pointer is now one character
 * after the occurence of @c uuid.
 *
 * @note This function @e assumes that the pattern being received is actually
 * an UUID. Dire things may happen otherwise because no checking beside length
 * is actually done.
 */
inline void __asimon_getstdin_upto(std::string& dest, char uuid[]) {
    size_t n = strlen(uuid);
    if (n != UUID_LENGTH) {
        quitf(_fail,
              "Internal critical error: expected an UUID with %d bytes; "
              "found a string with %d characters.",
              UUID_LENGTH, n);
    }

    // Basic KMP here. kmp[i] is the largest len <= i such that
    // uuid[0:len) = uuid(i-len:i]
    // (of course there is a trivial case where len = i+1 but that doesn't
    // matter)
    int kmp[UUID_LENGTH];
    memset(kmp, 0, sizeof(kmp));

    for (int i = 1; i < n; i++) {
        int j = kmp[i - 1];
        while (j && uuid[i] != uuid[j]) j = kmp[j - 1];
        if (uuid[i] == uuid[j]) j++;
        kmp[i] = j;
    }

    int k = 0;
    while (k != n) {
        char c = getc();
        if (c == EOF) {
            quitf(_fail,
                  "Internal critical error: no matching UUID was found.");
        }
        dest.push_back(c);

        while (k && uuid[k] != c) k = kmp[k - 1];
        if (uuid[k] == c) k++;
    }
    while (n--) dest.pop_back();
}

void __asimon_init_instream(InStream& stream, TMode mode) {
    stream.mode = mode;
    stream.stdfile = true;
    stream.strict = false;

    if (mode == _input) {
        stream.name = "input";
        _asimon_input.reserve(_ASIMON_STR_RESERVE);
        __asimon_getstdin_upto(_asimon_input, uuid1);
        stream.reader = new StringInputStreamReader(_asimon_input);
    } else if (mode == _answer) {
        stream.name = "answer";
        _asimon_answer.reserve(_ASIMON_STR_RESERVE);
        __asimon_getstdin_upto(_asimon_answer, uuid2);
        stream.reader = new StringInputStreamReader(_asimon_answer);
    } else {  // mode == _output
        stream.name = "output";
        _asimon_output.reserve(_ASIMON_STR_RESERVE);
        __asimon_getstdin_all(_asimon_output);
        stream.reader = new StringInputStreamReader(_asimon_output);
    }
}

void registerTestlibCmd(int argc, char* argv[]) {
    __testlib_ensuresPreconditions();
    __testlib_set_testset_and_group(argc, argv);
    TestlibFinalizeGuard::registered = true;

    testlibMode = _checker;
    __testlib_set_binary(stdin);

    std::vector<std::string> args(1, argv[0]);
    checker.initialize();

    int uuid_args = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp("--testset", argv[i])) {
            if (i + 1 < argc && strlen(argv[i + 1]) > 0)
                checker.setTestset(argv[++i]);
            else
                quit(_fail, std::string("Expected testset after --testset "
                                        "command line parameter"));
        } else if (!strcmp("--group", argv[i])) {
            if (i + 1 < argc)
                checker.setGroup(argv[++i]);
            else
                quit(
                    _fail,
                    std::string(
                        "Expected group after --group command line parameter"));
        } else if (!strcmp("--asimon_uuid1", argv[i])) {
            uuid_args++;
            if (i + 1 < argc) {
                strncpy(uuid1, argv[++i], UUID_LENGTH);
            } else
                quit(_fail,
                     std::string("Expected a version 4 UUID after "
                                 "--_asimon_uuid1 command line parameter"));
        } else if (!strcmp("--asimon_uuid2", argv[i])) {
            uuid_args++;
            if (i + 1 < argc) {
                strncpy(uuid2, argv[++i], UUID_LENGTH);
            } else
                quit(_fail,
                     std::string("Expected a version 4 UUID after "
                                 "--_asimon_uuid2 command line parameter"));
        } else
            args.push_back(argv[i]);
    }

    if (uuid_args != 2) {
        quitf(_fail,
              "Internal critical error: 2 UUID arguments expected, %d found.",
              uuid_args);
    }

    argc = int(args.size());
    if (argc > 1 && "--help" == args[1]) __testlib_help();

    // MUST be in input -> answer -> output order.
    __asimon_init_instream(inf, _input);
    __asimon_init_instream(ans, _answer);
    __asimon_init_instream(ouf, _output);
}

#endif