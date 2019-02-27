from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from utils import *


def find_next_button(browser, table_id):

    next_button = browser.find_element_by_id(table_id + "_next")

    return next_button


def is_next_page_available(browser, table_id):

    next_button = find_next_button(browser, table_id)

    next_button_class = next_button.get_attribute("class").split(" ")

    next_page = True

    if "disabled" in next_button_class:
        next_page = False

    return next_page


def extract_datables_table(url):

    path_to_chromedriver = "./chromedriver_win32/chromedriver.exe"
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    browser.get(url)

    year = extract_year(browser.find_element_by_tag_name("h1").text)

    data_table_id = "DataTables_Table_0"

    next_page_available = is_next_page_available(browser, data_table_id)

    list_states = []
    list_populations = []

    while next_page_available:

        table_html = browser.find_element_by_id(data_table_id + "_wrapper").get_attribute("outerHTML")
        div_table = BeautifulSoup(table_html, "html.parser")

        trs = div_table.find("table", {"id": data_table_id}).find("tbody").find_all("tr")

        for tr in trs:

            tds = tr.find_all("td")

            state = tds[1].text.strip()
            population = tds[2].text.strip()

            if RepresentsInt(population):
                list_populations.append(int(population))
            else:
                list_populations.append(None)

            list_states.append(state)

        find_next_button(browser, data_table_id).click()
        next_page_available = is_next_page_available(browser, data_table_id)

    browser.close()

    dataframe = pd.DataFrame({
        "stát": list_states,
        "rok": year,
        "populace": list_populations
    })

    return dataframe
