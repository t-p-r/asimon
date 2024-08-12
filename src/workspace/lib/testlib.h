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

std::string _name[3];
std::string _content[3];
int _sz[3];

/**
 * @brief Consumes @c __n bytes from @c stdin into a string @c dest.
 */
inline void __getstdin(std::string& dest, std::size_t __n) {
    dest.resize(__n);
    fread(&dest[0], sizeof(char), __n, stdin);
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
    stream.strict = false;  // and aren't validators

    __getstdin(_content[mode], _sz[mode]);
    stream.reader = new StringInputStreamReader(_content[mode]);
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
    using __testlib_asimon::_sz;

    for (int i = 1; i < argc; i++) {
        // Testsets and groups are handled on the Python side, no checking
        // is necessary here. The only thing needed to be parsed are the
        // sizes.
        if (!strcmp("--_asimon_sz_input", argv[i])) {
            _sz[_input] = atoi(argv[++i]);
        } else if (!strcmp("--_asimon_sz_answer", argv[i])) {
            _sz[_answer] = atoi(argv[++i]);
        } else if (!strcmp("--_asimon_sz_output", argv[i])) {
            _sz[_output] = atoi(argv[++i]);
        } else
            args.push_back(argv[i]);
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