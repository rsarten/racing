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

from sqlalchemy import create_engine
engine = create_engine(f"postgresql+psycopg2://rory:{password}@localhost:5432/horse_racing")

meets = pd.read_sql_query("select venue_id, \"date\" from racing.meets", engine, index_col="venue_id")
#venues = pd.read_sql_query("select * from racing.venues", engine, index_col="venue_id")
meets = meets.join(venues)
meets.reset_index(inplace=True)

def meets_links():
    site = "https://racingaustralia.horse"

    all_meets = meet_links()
    all_meets["date"] = all_meets.link.apply(date_from_link)
    all_meets['type'] = all_meets['meet_type'].replace(' \(Trial\)', '', regex=True)
    all_meets["link"] = site+all_meets.link
    all_meets["venue"] = all_meets.venue.apply(clean_venue)
    return all_meets
#professional # 227
#trial # 74
all_meets = meets_links()
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



all_meets = all_meets.merge(meets, on = ["name", "state_code", ""])

all_meets.columns



import psycopg2
conn = psycopg2.connect(database="horse_racing",
                        host="localhost",
                        user="rory",
                        password=password,
                        port="5432")
cursor = conn.cursor()
cursor.execute("select * from racing.venues where venue_id = 3")
cursor.fetchall()
cursor.execute("select * from racing.venues where venue_id = 18")
cursor.fetchall()
cursor.close()

venues = all_meets[["venue", "state"]]
venues.rename(columns={"venue":"name"}, inplace=True)
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


db_venues = pd.read_sql_query("select * from racing.venues", con=engine)
db_venues.rename(columns={"name": "venue", "state_code": "state"}, inplace=True)
db_venues.set_index(["venue", "state"], inplace=True)

def meet_details(meets):
    meet_ = {
        "venue": meets["venue"],
        "date": meets["full_date"],
        "type": meets["meet_type"],
        "link": meets["link"],
        "state": meets["state"]
    }
    if "details" in meets.keys():
        meet_["condition"] = meets["details"]["condition"],
        meet_["dual_track"] = meets["details"]["dual_track"],
        meet_["information"] = meets["details"]["information"],
        meet_["penetrometer"] = meets["details"]["penetrometer"],
        meet_["rail"] = meets["details"]["rail"],
        meet_["weather"] = meets["details"]["weather"]
    return meet_

meet_data = [meet_details(meet) for meet in meets]
meet_data = pd.DataFrame(meet_data)
meet_data.set_index(["venue", "state"], inplace=True)

m = meet_data.join(db_venues)
m.sort_values("date", inplace=True)
m.to_sql("meets", engine, index=False, if_exists="append", schema="racing")
m.condition.value_counts()

meets[4]["details"]["races"][0]["result"]

horses = []
for meet in meets:
    if "details" in meet.keys():
        if "races" in meet["details"].keys():
            for race in meet["details"]["races"]:
                result = race["result"]
                for res in result:
                    horses.append({"name": res["horse_name"], "code": res["code"]})
horses = pd.DataFrame(horses)
horses.to_sql("horses", engine, index=False, if_exists="append", schema="racing")

import json
from pprint import pprint
meets = json.load(open("data/meets.json"))
pprint(meets[1]["details"]c["races"])
meets[0].keys()
meets[1]["details"].keys()
venues = pd.read_csv("data/venues.csv")
venues.venue.apply(len).max()

pd.DataFrame(meets[1]["details"]["races"][0]["result"])
