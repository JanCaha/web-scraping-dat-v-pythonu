from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def next_page_url(soup):

    next = soup.find("ul", {"class": ["main-pager", "pager"]}).find("li", {"class": "next"})

    if next is not None:
        a = next.find("a")

        if a is not None:
            return a["href"]
        else:
            return None
    else:
        return None


def is_next_page(soup):

    if next_page_url(soup) is not None:
        return True
    else:
        return False

def load_url_soup(url):

    r = requests.Session().get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    return soup


def get_pages(url):

    soup = load_url_soup(url)

    main_url = re.search("https://[a-z]+\.[a-z]+\.[a-z]{2}", url).group(0)

    load_posts = True

    list_titles = []
    list_url = []
    list_type = []

    while load_posts:

        posts = soup.find("div", {"class": "posts-list"}).find_all("article")

        for post in posts:

            article_url = post.find_all("a")[0]["href"]
            article_url = main_url + article_url
            title = post.find("h2", {"class": "post-title"}).text
            type = post.find("div", {"class": "blog-tags"}).find("a").text

            list_titles.append(title)
            list_url.append(article_url)
            list_type.append(type)

        if is_next_page(soup):
            soup = load_url_soup(main_url + next_page_url(soup))
        else:
            load_posts = False

    dataframe = pd.DataFrame({
        "url": list_url,
        "titulek": list_titles,
        "typ": list_type
    })

    return dataframe