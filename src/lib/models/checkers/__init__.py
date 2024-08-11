"""
Test checkers for Worker class.
Some plugin init functions are executed here.
"""

from importlib import import_module
from pkgutil import iter_modules
from inspect import getmembers

from .base import CheckerResult, Checker

DISCOVERED_CHECKERS = {}
"""
Contains pairs `("name", "class")` where `name` is the return value of `class.__str__()`.

This enable a minimal checker plugin system: the user just need to derive a new class
from the base Checker class, give it an alias (through the __str__ function) and then use
this alias in the `checker` field in top-level config files.
"""


def _init_checkers():
    PACKAGE_LOCATION = __name__

    # dynamic import from source file
    checker_modules = [
        import_module(f"{PACKAGE_LOCATION}.{name}")
        for _, name, ___ in iter_modules(__path__)
        if name != "base"
    ]

    for checker_module in checker_modules:
        # crawl through all objects observable from checker source files
        for checker_class_name, __ in getmembers(checker_module):
            if (
                checker_class_name.endswith("Checker")
                and checker_class_name != "Checker"
            ):
                checker_class_obj = getattr(checker_module, checker_class_name)
                checker_alias = checker_class_obj.__str__()
                DISCOVERED_CHECKERS[checker_alias] = checker_class_obj  # magic


_init_checkers()
