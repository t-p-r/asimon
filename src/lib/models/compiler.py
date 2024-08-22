"""
C++ compiler wrapper with caching.
"""

from hashlib import sha256, file_digest
from pathlib import Path
from shutil import copy2
from subprocess import run

from lib.config.paths import cache_dir, workspace
from lib.utils.system import is_windows
from lib.utils.formatting import send_message, text_colors
from lib.utils.system import terminate_proc

from concurrent.futures import ProcessPoolExecutor, Future


MAX_CACHE_FILES = 64  # TODO: implements this
SUPPORTED_COMPILERS = ["g++", "clang++"]

DEFAULT_COMPILER_ARGS = {
    "g++": f"-pipe -Wall -O2 -I{workspace}",
}

if is_windows():
    # add stack option to G++ and Clang
    WIN_STACK_SIZE = 268435456  # on Linux this is effectively infinite
    DEFAULT_COMPILER_ARGS["g++"] += f" -static -Wl,--stack={WIN_STACK_SIZE}"  # mind the gap

    # add MSVC compiler
    SUPPORTED_COMPILERS.append("cl")
    DEFAULT_COMPILER_ARGS["cl"] = f"/EHsc /W4 /O2 /I{workspace} /F{WIN_STACK_SIZE}"

DEFAULT_COMPILER_ARGS["clang++"] = DEFAULT_COMPILER_ARGS["g++"]  # thanks Clang team


class Compiler:
    @staticmethod
    def probe(compiler: str) -> bytes | None:
        """
        Invoke the compiler's version specifier to see if it exists.
        If it does, returns the output. This will be used for SHA256 hashing later on.
        """
        try:
            proc = run([compiler, "--version"], check=True, capture_output=True)  # G++, Clang
            return proc.stdout
        except Exception:
            pass

        try:
            proc = run(compiler, check=True, capture_output=True)  # MSVC
            return proc.stdout
        except Exception:
            pass

        return None

    @staticmethod
    def init_msvc():
        """TODO: find and run MSVC init batch file."""
        pass

    def __init__(self, compilation_command: str | None = None, cpu_workers: int = 1):
        """
        Initialize the compiler.

        `compilation_command` must be a string,
        being either:
        - `"$default"` or an empty string: ASIMON will find the compiler and appends its
        default compilation args.
        - `"g++ $default"`: ASIMON will attempts to use the G++ compiler and appends its
        default compilation args.
        - `"clang++ $default"`, `"cl $default`: same as above but for the Clang and MSVC++
        compilers.
        - Any other string: ASIMON will interpret the first token as the compiler
        and the rest as arguments.

        `cpu_workers` is the number of concurrent compilation process.
        """
        self.cpu_workers = max(4, cpu_workers)  # what can go wrong?

        def autodetect_compiler():
            for compiler in SUPPORTED_COMPILERS:
                ver = self.probe(compiler)
                if ver is not None:
                    self.compiler = compiler
                    self.compiler_args = DEFAULT_COMPILER_ARGS[compiler]
                    send_message(f"Autodetected C++ compiler: {compiler}.", text_colors.YELLOW)
                    return ver

            terminate_proc(
                "Fatal error: No C++ compiler found. "
                + "Installation is the user's responsibility (see install.md for a start)."
            )

        if compilation_command == "$default" or compilation_command == "":
            autodetect_compiler()
        else:
            self.compiler = compilation_command.split()[0]  # first token
            self.compiler_args = " ".join(compilation_command.split()[1:])  # everything after that

        self.compiler_ver = self.probe(self.compiler)
        if self.compiler_ver is None:
            send_message(
                "The specified compiler is not found, falling back to autodetect mode...",
                text_colors.YELLOW,
            )
            self.compiler_ver = autodetect_compiler()

        if self.compiler not in SUPPORTED_COMPILERS:
            terminate_proc("Fatal error: C++ compiler not supported.")

        if self.compiler_args == "$default" and self.compiler in SUPPORTED_COMPILERS:
            self.compiler_args = DEFAULT_COMPILER_ARGS[self.compiler]

    def compile_file(self, source_path: Path, output_path: Path):
        """
        Call the compiler. The caching process is done here.

        First preprocess the file in `source_path`. Then create a SHA256 from:
        - the content of the preprocessed source code
        - the compilation args
        - the compiler version

        If these three things stay the same then the resulting binary file will also does.
        The rest are just paperwork.
        """

        # Preprocess source code (since included libs can change)
        prep_flag = "/P" if self.compiler == "cl" else "-E"
        prep_output_flag = "/Fi" if self.compiler == "cl" else "-o"
        run(
            f"{self.compiler} {self.compiler_args} {prep_flag} {source_path} {prep_output_flag} {output_path}".split(),
            check=True,
        )

        hash_obj = sha256()
        with open(output_path, "rb") as preprocessed_source:
            hash_obj = file_digest(preprocessed_source, "sha256")

        hash_obj.update(bytearray(self.compiler_args, "utf-8"))
        hash_obj.update(self.compiler_ver)

        cache_path = cache_dir / f"{hash_obj.hexdigest()}.exe"
        if cache_path.exists():
            send_message(
                f"Cached executable for {source_path.name} found, skipping compilation...",
                text_colors.YELLOW,
            )
            # If the metadata is not properly carried over then Microsoft Security will engage thinking that
            # output_path is a trojan.
            copy2(cache_path, output_path)
        else:
            # MSVC has /Fe instead of /Fi.
            # See: https://learn.microsoft.com/en-us/cpp/build/reference/compiler-options-listed-by-category.
            bin_output_flag = "/Fe" if self.compiler == "cl" else "-o"
            run(
                f"{self.compiler} {self.compiler_args} {source_path} {bin_output_flag} {output_path}".split(),
                check=True,
            )
            copy2(output_path, cache_path)

    def __call__(self, source_output: list[tuple[Path, Path]]):
        """
        Call the compiler for all items in `source_output`.

        `source_output` must be a list where each item is `(source, output)`,
        corresponding to the locations of the C++ source file
        and its executable, respectively.
        """

        send_message(
            "Compiling source codes, warnings and/or errors may be shown below...",
            text_colors.GREEN,
        )

        with ProcessPoolExecutor(max_workers=self.cpu_workers) as worker_pool:
            procs: list[tuple[Path, Future]] = []
            for source_path, output_path in source_output:
                procs.append(
                    (source_path, worker_pool.submit(self.compile_file, source_path, output_path))
                )
            for source_path, result_obj in procs:
                if result_obj.exception() is not None:  # compiler fails
                    terminate_proc(
                        f"Fatal error: C++ source file {source_path.name} cannot be compiled, or doesn't exist.",
                    )
