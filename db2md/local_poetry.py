import os
from typing import List


def create_folders(folders: List[str]):
    """Create a folder for each category of poem.

    Keyword arguments:
    folders -- list of macro categories names.
    """
    os.chdir(os.getcwd() + "\\poemas")
    for folder in folders:
        os.mkdir(folder)

    os.chdir("..")


def get_local_poem_types() -> List[str]:
    """Return a set with current poetry folders in directory."""
    os.chdir(os.getcwd() + "\\poemas")
    list_dir = os.listdir()
    setdir = list(set(list_dir))

    os.chdir("..")

    return setdir


def get_local_poem(poem_types: List[str]) -> List[str]:
    """Return a list of poetrys names.

    Keywword arguments:
    poem_types -- set of folders names.
    """
    os.chdir(os.getcwd() + "\\poemas")
    cwd = os.getcwd()
    poems = []

    for type in poem_types:
        os.chdir(f"{cwd}\\{type}")
        poems.extend(os.listdir())

    os.chdir("..")

    poems = [poem.split(".md")[0] for poem in poems]

    return poems
