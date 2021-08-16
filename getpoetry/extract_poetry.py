from getpoetry.helpers import exception_handler, get_env, print_message
from getpoetry.local_poetry import get_local_poem, get_local_poem_types
from time import sleep
from random import random
from typing import Dict, List
from selenium.webdriver import Chrome


class Extract:
    def __init__(self, browser, local_poems):
        self.browser = browser
        _, er = self.login()
        pages, er = self.get_pages()
        print(pages)
        poems_href, er = self.get_poems_href(pages)
        print(poems_href)

    @exception_handler
    def login(self):
        """Login into Recanto das Letras"""
        browser.get("https://www.recantodasletras.com.br/escrivaninha/login/login.php?")
        sleep(1 + random())

        page_element_login = self.browser.find_element_by_class_name("login-form-inner")

        user = page_element_login.find_element_by_name("usuario")
        user.click()
        sleep(0.5 + random())
        user.send_keys(get_env("user"))
        sleep(0.5 + random())

        password = page_element_login.find_element_by_name("senha")
        password.click()
        sleep(0.5 + random())
        password.send_keys(get_env("password"))
        sleep(0.5 + random())

        login_button = page_element_login.find_element_by_name("imageField")
        login_button.click()

    @exception_handler
    def get_pages(self) -> List[str]:
        """Return an list of pages with poems."""
        pages = ["https://www.recantodasletras.com.br/escrivaninha/publicacoes/index.php"]
        self.browser.get(pages[0])
        index = self.browser.find_element_by_class_name("index-pagination-descr")
        max_pages = int(index.text.split(" ")[-1].split(":")[0])
        for i in range(2, max_pages + 1):
            pages.append(
                f"https://www.recantodasletras.com.br/escrivaninha/publicacoes/index.php?pag={i}"
            )

        return pages

    @exception_handler
    def get_poems_href(self, pages: List[str]) -> List[Dict[str, str]]:
        """Return an list of dictionaries with title and href of each poem.

        Keyword arguments:
        pages -- List of pages."""
        poems = []

        for page in pages:
            self.browser.get(page)
            sleep(1 + random())
            titles = self.browser.find_elements_by_class_name("index-title")[1:]
            categories = self.browser.find_elements_by_class_name("index-category")
            dates = self.browser.find_elements_by_class_name("index-date")
            views = self.browser.find_elements_by_class_name("index-views")

            for title, category, date, view in zip(titles, categories, dates, views):
                poem = {}
                p = title.find_element_by_tag_name("a")
                poem["title"] = p.text
                poem["href"] = p.get_attribute("href")
                poem["category"] = category.text
                poem["date"] = date.text
                poem["views"] = view.text
                poems.append(poem)

        return poems


if __name__ == "__main__":
    poem_types = get_local_poem_types()
    print_message(
        "Local Styles",
        ", ".join(poem_types),
        "s",
    )
    local_poems = get_local_poem(poem_types)
    print_message(
        "Local Poems",
        " ".join(local_poems),
        "s",
    )

    browser = Chrome()
    ext = Extract(browser, local_poems)
