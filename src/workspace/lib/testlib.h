/**
 * ASIMON: Compatibility layer for testlib.h.
 *
 * This file redefines the original (vanilla) testlib's @c registerTestlibCmd
 * function to correspond with ASIMON's external checker protocol. In particular,
 * it initializes the three standard @c InStream objects in such a way that they
 * are fed contents from @c stdin and not files.
 *
 * THIS FILE DOES NOT, IN ANY WAY, IMPLEMENTS EVEN A FUNCTIONAL SUBSET OF
 * TESTLIB.H, NOR INDUCE ANY CHANGES ON THE USER'S SIDE, BUT MERELY ADD A
 * COMPATIBILITY LAYER SO THAT THE ORIGINAL VERSION OF TESTLIB.H CAN WORK WITH
 * ASIMON'S FILELESS I/O POLICY.
 *
 *
 * It is imperative that the original testlib repository be included in the folder
 * containing this file. Do this if you have not done so after installing
 * ASIMON:
 *          $ git submodule update --init

 * to initialize the submodules, including testlib.
 *
 * If you don't want to do so, head to this directory and directly clone testlib
 * from source:
 *          $ git clone https://github.com/MikeMirzayanov/testlib/
 *
 *
 * @file /src/workspace/lib/testlib.h
 */

#ifndef TESTLIB_ASIMON
#define TESTLIB_ASIMON

/* Overrides vanilla testlib's registerTestlibCmd. */
#define registerTestlibCmd __registerTestlibCmd_vanilla
#include "testlib/testlib.h"
#undef registerTestlibCmd

namespace __testlib_asimon {

static const size_t UUID_LENGTH = 36;                // 32 chars + 4 `-`
static const size_t STR_RESERVE = 32 * 1024 * 1024;  // 32MB

std::string _name[3];
std::string _content[3];

char _uuid[3][UUID_LENGTH];

/**
 * @brief Get the next byte from @c stdin, or return @a EOF if stdin
 * is empty.
 *
 * @note Use @c fread() to perform efficient bulk reading.
 */
uint8_t __getc() noexcept {
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
inline void __getstdin_all(std::string& dest) {
    for (char c = __getc(); c != EOF; c = __getc()) dest.push_back(c);
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
inline void __getstdin_upto(std::string& dest, char uuid[]) {
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
    // matter).
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
        char c = __getc();
        if (c == EOF) quitf(_fail, "Internal critical error: no matching UUID was found.");
        dest.push_back(c);
        while (k && uuid[k] != c) k = kmp[k - 1];
        if (uuid[k] == c) k++;
    }

    while (n--) dest.pop_back();
}

/**
 * @brief Initialize a testlib @c InStream.
 *
 * @param stream The @c InStream in question.
 * @param mode The @c TMode (aka type ID) of `stream`. Must be one of: `_input`, `_answer`, `_output`.
 *
 * @note Use vanilla testlib's @c StringInputStreamReader. Thanks, Mike.
 */
void __init_instream(InStream& stream, TMode mode) {
    stream.mode = mode;
    stream.name = _name[mode];
    stream.stdfile = true;  // all are from stdin
    stream.strict = false;  // no validator here

    std::string& content = _content[mode];
    content.reserve(STR_RESERVE);

    if (mode == _output)
        __getstdin_all(content);
    else
        __getstdin_upto(content, _uuid[mode]);

    stream.reader = new StringInputStreamReader(content);
}

}  // namespace __testlib_asimon

/**
 * @brief Testlib register for checker programs.
 *
 * @note It is highly recommended that this function is the first one executed
 * in @c main().
 */
void registerTestlibCmd(int argc, char* argv[]) {
    __testlib_ensuresPreconditions();
    __testlib_set_testset_and_group(argc, argv);
    TestlibFinalizeGuard::registered = true;

    testlibMode = _checker;
    __testlib_set_binary(stdin);

    std::vector<std::string> args(1, argv[0]);
    checker.initialize();

    using __testlib_asimon::__init_instream;
    using __testlib_asimon::_name;
    using __testlib_asimon::_uuid;
    using __testlib_asimon::UUID_LENGTH;

    int uuid_args = 0;
    for (int i = 1; i < argc; i++) {
        // Testsets and groups are handled on the Python side, no checking
        // is necessary here. The only thing needed to be parsed are the
        // UUIDs.
        if (!strcmp("--asimon_uuid1", argv[i])) {
            uuid_args++;
            if (i + 1 < argc) {
                strncpy(_uuid[_input], argv[++i], UUID_LENGTH);
            } else
                quit(_fail, std::string("Expected a version 4 UUID after "
                                        "--_uuid1 command line parameter"));
        } else if (!strcmp("--asimon_uuid2", argv[i])) {
            uuid_args++;
            if (i + 1 < argc) {
                strncpy(_uuid[_answer], argv[++i], UUID_LENGTH);
            } else
                quit(_fail, std::string("Expected a version 4 UUID after "
                                        "--_uuid2 command line parameter"));
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

    // MUST be in ASIMON's input -> answer -> output order.
    _name[_input] = "input";
    _name[_answer] = "answer";
    _name[_output] = "output";

    __init_instream(inf, _input);
    __init_instream(ans, _answer);
    __init_instream(ouf, _output);
}

#endif /* TESTLIB_ASIMON */