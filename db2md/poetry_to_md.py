from datetime import datetime
from getpoetry.helpers import print_message
from getpoetry.psql.main import read_db
from getpoetry.local_poetry import (
    create_folders,
    get_local_poem,
    get_local_poem_types,
)
import os
import pandas as pd
from typing import List


def write_poems_md(poem_categories: List[str], data: pd.DataFrame):
    os.chdir(os.getcwd() + "\\poemas")

    for category in poem_categories:
        os.chdir(os.getcwd() + "\\" + f"{category}")
        poems_to_write = data.loc[data["category"] == category]

        for idx in range(len(poems_to_write)):
            with open(f"{poems_to_write.iloc[idx]['title_formatted']}.md", "w") as f:
                f.write(format_md(poems_to_write.iloc[idx]))

        os.chdir("..")

    os.chdir("..")


def format_md(poem: pd.Series) -> str:
    text_list = []

    # Title
    text_list.append("".join([f"### {poem['title']}  ", "\n"]))

    # Text
    poem_text = poem["text"].replace("\n", "  ")
    text_list.append(f"{poem_text}")

    # Separator
    text_list.append("\n---")

    # Date
    text_list.append(
        "".join(["_data: ", datetime.strftime(poem["date"][0], "%d/%m/%Y"), "_"])
    )

    # Category
    text_list.append("".join(["_estilo: ", poem["category"], "_"]))

    # Join
    text = "".join(text_list)

    return text


if __name__ == "__main__":
    df = read_db("poems")
    df["title_formatted"] = df.apply(
        lambda row: "_".join(row["title"].split(" ")).lower(), axis=1
    )
    categories = df["category"].unique()
    macro_categories = [
        category if ">" not in category else category.split()[0]
        for category in categories
    ]

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
