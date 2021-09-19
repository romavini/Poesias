from datetime import datetime
import os
import pandas as pd
from typing import List


def write_poems_md(poem_categories: List[str], data: pd.DataFrame):
    for category in poem_categories:
        os.chdir(os.getcwd() + "\\" + f"{category}")
        poems_to_write = data.loc[data["category"] == category]

        for idx in range(len(poems_to_write)):
            with open(f"{poems_to_write.iloc[idx]['title_formatted']}.md", "w") as f:
                f.write(format_md(poems_to_write.iloc[idx]))

        os.chdir("..")


def format_md(poem: pd.Series) -> str:
    text_list = []

    # Title
    text_list.append("".join([f"### {poem['title']}  ", "\n"]))

    # Text
    text_list.append(f"{poem['text']}")

    # Separator
    text_list.append("\n---")

    # Date
    text_list.append(
        "".join(["\n_data: ", datetime.strftime(poem["date"], "%d/%m/%Y"), "_"])
    )

    # Category
    text_list.append("".join(["\n_estilo: ", poem["category"], "_"]))

    # Join
    text = "".join(text_list)

    return text
