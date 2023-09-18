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

from src.export.connections import get_engine, get_connection

engine = get_engine(password)
conn = get_connection(password)

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
    print(meet["date"], ":", meet["venue"])
    try:
        meet_details = extract_meet_details(meet_url)
        #meet_details["races"] = extract_race_details(meet_url)
        meet["details"] = meet_details
    except:
        print("failed to scrape meet")

def meet_details(meets):
    meet_ = {
        "venue": meets["venue"],
        "date": meets["date"],
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

for meet in meets[:2]:
    meet_table = meet_details(meet)
    m_tab = pd.DataFrame(meet_table)
    print(meet_table)

cursor = conn.cursor()
cursor.execute("select * from racing.venues where venue_id = 3")
cursor.fetchall()

venue = meet_table["venue"]
state = meet_table["state"]
date = meet_table["date"]

import psycopg2
conn = psycopg2.connect(database="horse_racing",
                        host="localhost",
                        user="rory",
                        password=password,
                        port="5432")


with conn.cursor() as cursor:
    cursor.execute(f"select venue_id from racing.venues where \"state\" = \'{state}\' and \"name\" = \'{venue}\';")
    venue_id = cursor.fetchone()

    if venue_id == None:
        print("adding venue")
        venue_df = pd.DataFrame({"state": [state], "name": [venue]})
        venue_df.to_sql("venues", engine, index=False, if_exists="append", schema="racing")

        #cursor.execute(f"insert into racing.venues(\"name\", \"state\") values ('{venue}', '{state}');")
        cursor.execute(f"select venue_id from racing.venues where \"state\" = \'{state}\' and \"name\" = \'{venue}\';")
        venue_id = cursor.fetchone()
        
    print(venue_id)

conn.close()


venue_id[0]
