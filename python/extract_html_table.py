import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import *


def extract_html_table(url):

    r = requests.Session().get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    h1 = soup.find("h1").text

    year = re.search("[0-9]{4}", h1).group(0)

    table_body = soup.find("table").find("tbody")

    rows = table_body.find_all("tr")

    list_states = []
    list_populations = []

    for row in rows:

        tds = row.find_all("td")

        state = tds[0].text.strip()
        population = tds[1].text.strip()

        if RepresentsInt(population):
            list_populations.append(int(population))
        else:
            list_populations.append(None)

        list_states.append(state)

    dataframe = pd.DataFrame({
        "stát": list_states,
        "rok": year,
        "populace": list_populations
    })

    return dataframe
