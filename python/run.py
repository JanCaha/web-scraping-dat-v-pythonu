import pandas as pd
from extract_datatables_table import extract_datables_table
from extract_html_table import extract_html_table
from get_pages import get_pages

# testing url
# url = "http://127.0.0.1:4000/web-scraping-dat-v-pythonu/"

# online url
url = "https://jancaha.github.io/web-scraping-dat-v-pythonu/"

pages = get_pages(url)

data_frames = []

for index, row in pages.iterrows():

    if row["typ"] == "datatables":
        data_frames.append(extract_datables_table(row["url"]))
    else:
        data_frames.append(extract_html_table(row["url"]))

result = pd.concat(data_frames)

result.to_csv("data.csv", index=False)
