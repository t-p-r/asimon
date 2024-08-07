"""
C++ compiler wrapper.
"""

# TODO: cache compiled programs.

from lib.utils.system import is_windows
from lib.utils.formatting import send_message
from lib.utils.formatting import text_colors
from lib.utils.system import terminate

from lib.config.paths import cache_dir, workspace
from subprocess import run, Popen
from pathlib import Path

SUPPORTED_COMPILERS = ["g++", "clang++"]
STDCPP_VERSION = "c++20"

DEFAULT_COMPILER_ARGS = {
    "g++": f"-pipe -DONLINE_JUDGE -O2 -std={STDCPP_VERSION} -I{workspace}",
    "clang++": f"-pipe -DONLINE_JUDGE -O2 -std={STDCPP_VERSION} -I{workspace}",
}

if is_windows():
    # add stack option to G++ and Clang
    WIN_STACK_SIZE = 268435456  # Codeforces stack size (on Linux this is effectively infinite)
    DEFAULT_COMPILER_ARGS["g++"] += f" -static -Wl, --stack={WIN_STACK_SIZE}"  # mind the gap
    DEFAULT_COMPILER_ARGS["clang++"] += f" -static -Wl, --stack={WIN_STACK_SIZE}"
    # add MSVC compiler
    SUPPORTED_COMPILERS.append("cl")
    DEFAULT_COMPILER_ARGS["cl"] = (
        f"/EHsc /DONLINE_JUDGE /W4 /O2 /std:{STDCPP_VERSION} /I{workspace} /F{WIN_STACK_SIZE}"
    )


class Compiler:
    @staticmethod
    def probe(compiler: str) -> bool:
        """Invoke the compiler's version specifier to see if it exists."""
        try:
            run([compiler, "--version"], check=True, capture_output=True)  # G++, Clang
            return True
        except Exception:
            pass

        try:
            run(compiler, check=True, capture_output=True)  # MSVC
            return True
        except Exception:
            pass

        return False

    def __init__(
        self,
        compilation_command: str | None = None,
    ):
        """
        Initialize the compiler.

        Up to one argument is accepted. This argument must be a string,
        being either:
        - `"$default"` or an empty string: ASIMON will find the compiler and appends its
        default compilation args.
        - `"g++ $default"`: ASIMON will attempts to use the G++ compiler and appends its
        default compilation args.
        - `"clang++ $default"`, `"cl $default`: same as above but for the Clang and MSVC++
        compilers.
        - Any other string: ASIMON will interpret the first token as the compiler
        and the rest as arguments.
        """

        def autodetect_compiler():
            for compiler in SUPPORTED_COMPILERS:
                if self.probe(compiler):
                    self.compiler = compiler
                    self.compiler_args = DEFAULT_COMPILER_ARGS[compiler]
                    send_message(f"Autodetected compiler: {compiler}.", text_colors.YELLOW)
                    return
            terminate(
                "Fatal error: No C++ compiler found. "
                + "Installation is the user's responsibility (see install.md for a start)."
            )

        if compilation_command == "$default" or compilation_command == "":
            autodetect_compiler()
        else:
            tokens = compilation_command.split()
            self.compiler = tokens[0]
            self.compiler_args = ' '.join(tokens[1:])

        if not self.probe(self.compiler):
            send_message(
                "The specified compiler is not found, falling back to autodetect mode...",
                text_colors.YELLOW,
            )
            autodetect_compiler()

        if self.compiler not in SUPPORTED_COMPILERS:
            send_message(
                "Compiler not supported (though ASIMON will try to run it as if it is G++). "
                + "You're on your own now. Good luck.",
                text_colors.YELLOW,
            )

        if self.compiler_args == "$default" and self.compiler in SUPPORTED_COMPILERS:
            self.compiler_args = DEFAULT_COMPILER_ARGS[self.compiler]

    def __call__(self, source_output: list[tuple[Path, Path]]):
        """
        Call the compiler.

        `source_output` must be a list where each item is `(source, output)`,
        corresponding to the locations of the C++ source file
        and its executable, respectively.
        """

        send_message(
            "Compiling source codes, warnings and/or errors may be shown below...",
            text_colors.GREEN,
        )

        procs: list[tuple[Path, Popen]] = []
        for source_path, output_path in source_output:
            COMPILATION_SYNTAX = {
                "g++": f"g++ {self.compiler_args} {source_path} -o {output_path}",
                "clang++": f"clang++ {self.compiler_args} {source_path} -o {output_path}",
                "cl": f"cl {self.compiler_args} {source_path} /Fe {output_path}",
            }
            procs.append(
                (
                    source_path,
                    Popen(
                        COMPILATION_SYNTAX[
                            self.compiler if self.compiler in SUPPORTED_COMPILERS else "g++"
                        ].split()
                    ),
                )
            )
        for source_path, popen_obj in procs:
            if popen_obj.wait() != 0:  # à la returncode
                terminate(
                    f"Fatal error: C++ source file {source_path} cannot be compiled, or doesn't exist.",
                )
