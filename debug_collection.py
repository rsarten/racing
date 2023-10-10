import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_races
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.export.table_work import add_venue, add_entry
from src.model.structs import Meet

password=
engine = get_engine(password)
conn = get_connection(password)

meets = pd.read_sql_query("select * from racing.meets where meet_type = 'Professional' and \"status\" = 'error: scrape meet'", engine)


meets = meets.to_dict(orient="records")
meet = meets[1]
meet["status"]
del meet["status"]

meet = Meet(**meet)
meet = extract_races(meet)

import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from bs4 import BeautifulSoup

url = "https://racingaustralia.horse/FreeFields/Results.aspx?Key=2023Sep17,NSW,Armidale,Trial"

page = requests.get(meet.link, verify = False)
#page = requests.get(url, verify = False)
soup = BeautifulSoup(page.content, "html.parser")

def print_race(race):
    print(race.text.split(" - ")[0].replace("\n", ""))

race1 = soup.find("table", class_ = "race-title")
if race1 is None:
    return list()

next = race1.find_next_sibling()
next.name == "br"


race1 is None
race1.text.split(" - ")[0].replace("\n", "")
race2 = race1.find_next("table", class_ = "race-title")
race3 = race2.find_next("table", class_ = "race-title")
race4 = race3.find_next("table", class_ = "race-title")
race5 = race4.find_next("table", class_ = "race-title")
race6 = race5.find_next("table", class_ = "race-title")
race7 = race6.find_next("table", class_ = "race-title")
race8 = race7.find_next("table", class_ = "race-title")
race8 is None
race9 = race8.find_next("table", class_ = "race-title")
race5.find_next_sibling().find_next_sibling()


