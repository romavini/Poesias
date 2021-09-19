from db2md.poetry_to_md import write_poems_md
import os
from db2md.local_poetry import create_folders, get_local_poem, get_local_poem_types
from db2md.helpers import get_env, print_message, remove_separator
from db2md.psql.database import read_db


def main():
    df = read_db("poems")
    df["title_formatted"] = df.apply(
        lambda row: remove_separator("_".join(row["title"].split(" ")).lower()), axis=1
    )
    categories = df["category"].unique()
    macro_categories = [
        category if ">" not in category else category.split()[0]
        for category in categories
    ]

    os.chdir(get_env("poetry_folder_path"))
    poem_categories = get_local_poem_types()
    print_message(
        "Local Styles",
        ", ".join(poem_categories),
        "s",
    )
    categories_to_create = list(set(macro_categories) - set(poem_categories))

    create_folders(categories_to_create)

    local_poems = get_local_poem(poem_categories)
    print_message(
        "Info",
        f"{len(local_poems)} local poems, {len(df) - len(local_poems)} to be add.",
        "s",
    )

    write_poems_md(categories, df)


if __name__ == "__main__":
    main()
