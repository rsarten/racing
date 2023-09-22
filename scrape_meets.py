import numpy as np
import pandas as pd

import re
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from bs4 import BeautifulSoup

from src.scrape.extract_records import meet_links, extract_meet_details, extract_race_details
from src.scrape.utils import date_from_link

from datetime import datetime, timedelta
import time

scraped = pd.read_csv("data/meet_links.csv", index_col = False)
scraped.sort_values("date", ascending=False, inplace = True)
venues = scraped.drop_duplicates(["venue", "state"])
venues = venues[["venue", "state", "date"]]

site = "https://racingaustralia.horse"

meets = venues.to_dict(orient = "records")

with open('data/meets_2022.csv', 'a') as f:
    f.write('venue,state,date,link\n')

date_list = pd.date_range(start="2022-01-01",end="2022-12-31")
date_formatted = [d.strftime("%Y%b%d") for d in date_list]

for meet in meets:
    state = meet["state"]
    venue = meet["venue"]

    print(venue)

    for mod_date in date_formatted:
        time.sleep(1)
        url = f"{site}/FreeFields/Results.aspx?Key={mod_date},{state},{venue}"
        page = requests.get(url, verify = False)
        soup = BeautifulSoup(page.content, "html.parser")
        race_number_menu = soup.find("div", id = "race-number-menu")
        if race_number_menu is not None:
            with open('data/meets_2022.csv', 'a') as f:
                f.write(f'{venue},{state},{date_from_link(url)},"{url}"\n')

