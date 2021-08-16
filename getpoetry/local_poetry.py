import os
from typing import List


def get_local_poem_types() -> List[str]:
    """Return a set with current poetry folders in directory."""
    list_dir = os.listdir()
    setdir = [dir for dir in list_dir if "." not in dir]
    setdir = list(set(setdir) - set(["venv", "venvw", "getpoetry"]))

    return setdir


def get_local_poem(poem_types: List[str]) -> List[str]:
    """Return a list of poetrys names.

    Keywword arguments:
    poem_types -- set of folders names.
    """
    cwd = os.getcwd()
    poems = []

    for type in poem_types:
        os.chdir(f"{cwd}\\{type}")
        poems.extend(os.listdir())

    return poems
