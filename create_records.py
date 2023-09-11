import numpy as np
import pandas as pd

import os
import re
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from bs4 import BeautifulSoup

from src.scrape.extract_records import meet_links, extract_meet_details, extract_race_details
from src.scrape.utils import date_from_link, clean_venue

def update_meets_links(save_as = "data/all_state_meets.csv", write_out = True):
    site = "https://racingaustralia.horse"

    all_meets = meet_links()
    all_meets["full_date"] = all_meets.link.apply(date_from_link)
    all_meets['meet_type'] = all_meets['meet_type'].replace(' \(Trial\)', '', regex=True)
    all_meets["link"] = site+all_meets.link
    all_meets["venue"] = all_meets.venue.apply(clean_venue)

    if os.path.isfile(save_as):
        current_meets = pd.read_csv(save_as)
        combined_meets = pd.concat([all_meets, current_meets])
    else:
        combined_meets = all_meets

    combined_meets = combined_meets.drop_duplicates()
    if write_out:
        combined_meets.to_csv(save_as, index = False)
    return combined_meets
#professional # 227
#trial # 74
all_meets = update_meets_links()

from sqlalchemy import create_engine
engine = create_engine(f"postgresql+psycopg2://rory:{password}@localhost:5432/horse_racing")

venues = all_meets[["venue", "state"]]
venues.rename(columns={"venue":"name", "state":"state_code"}, inplace=True)
venues.to_sql("venues", engine, index=False, if_exists="append", schema="racing")

meets = all_meets.to_dict(orient = "records")
for meet in meets:
    meet_url = meet["link"]
    print(meet["full_date"], ":", meet["venue"])
    try:
        meet_details = extract_meet_details(meet_url)
        meet_details["races"] = extract_race_details(meet_url)
        meet["details"] = meet_details
    except:
        print("failed to scrape meet")

engine.dispose()

import json
with open('data/meets.json', 'w') as f:
    json.dump(meets, f)


import json
from pprint import pprint
meets = json.load(open("data/meets.json"))
pprint(meets[1])

venues = pd.read_csv("data/venues.csv")
venues.venue.apply(len).max()

pd.DataFrame(meets[1]["details"]["races"][0]["result"])
