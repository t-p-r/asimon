/**
 * ASIMON: Compatibility layer for testlib.h.
 *
 * THIS FILE DOES NOT, IN ANY WAY, IMPLEMENTS THE ENTIRETY OF TESTLIB.H,
 * BUT MERELY ADD A COMPATIBILITY LAYER SO THAT THE ORIGINAL VERSION
 * OF TESTLIB.H CAN WORK IN FILELESS MODE.
 *
 * It is imperative that the original testlib repo be included in the folder
 * containing this file. Do this if you have not done so after installing ASIMON:
 * 
 *          $ git submodule update --init
 * 
 * to initialize the submodules, including testlib.
 *
 *
 *
 * @file /src/workspace/lib/testlib.h
 */

#ifndef TESTLIB_ASIMON
#define TESTLIB_ASIMON

/* Overrides certain functions from testlib */
#define registerTestlibCmd __registerTestlibCmd_deprecated
#include "testlib/testlib.h"
#undef registerTestlibCmd

void registerTestlibCmd(int argc, char* argv[]) {
    // stub
    // TODO:
}

#endif