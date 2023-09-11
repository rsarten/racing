import numpy as np
import pandas as pd

import re
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from bs4 import BeautifulSoup

site = "https://racingaustralia.horse"

meet_attrs = [
    ('rail', r'(?<=Rail Position: ).*(?=Dual Track)'),
    ('dual_track', r'(?<=Dual Track Meeting: ).*(?=Track Type)'),
    ('track_type', r'(?<=Track Type: ).*(?=Track Condition)'),
    ('condition', r'(?<=Track Condition: ).*(?=Weather)'),
    ('weather', r'(?<=Weather: ).*(?=Penetrometer)'),
    ('penetrometer', r'(?<=Penetrometer: ).*(?=Track Information)'),
    ('information', r'(?<=Track Information: ).*')
]

def meet_overview(meet):
    tds = meet.find_all("td")
    meet_data = {
        "short_date": tds[0].text,
        "venue": tds[1].text.split(" - ")[0],
        "meet_type": tds[1].text.split(" - ")[1],
        "link": tds[1].find("a")['href']
    }
    return meet_data

def meet_links(states = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']):
    state_results = []
    for state in states:
        print("--------", state, "--------")
        state_url = f"{site}/FreeFields/Calendar_Results.aspx?State={state}"
        page = requests.get(state_url, verify = False)
        state_history = BeautifulSoup(page.content, "html.parser")

        meets = state_history.find("table", class_="race-fields").find_all("tr")
        for meet in meets[1:]:
            details = meet_overview(meet)
            details["state"] = state
            state_results.append(details)
        
    return pd.DataFrame(state_results)

def extract_meet_details(url):
    meet = {}

    page = requests.get(url, verify = False)
    soup = BeautifulSoup(page.content, "html.parser")

    race_venue = soup.find("div", class_ = "race-venue")
    banner = race_venue.text.replace('\r', '').replace('\n', '').replace('\t', '')

    date_pattern = r'(?<=, ).*(?=Meeting)'
    meet["date"] = re.findall(date_pattern, banner)[0]

    race_venue_bottom = soup.find("div", class_ = "race-venue-bottom").find("div", class_ = "col1").text
    for attr in meet_attrs:
        finds = re.findall(attr[1], race_venue_bottom)
        if len(finds) > 0:
            meet[attr[0]] = finds[0]
        else:
            meet[attr[0]] = None

    return meet

def extract_race_meta_details(race_details: BeautifulSoup):
    details = race_details.find("th").text.split('\r')[0]
    race = {
        "race_number": int(re.findall(r'(?<=^Race )\d*', details)[0]),
        "race_time": re.findall(r'[\d:AP]+M', details)[0],
        "race_distance": int(re.findall(r'(?<=\()\d+(?= METRES)', details)[0])
    }

    track_name_pattern = r'(?<=Track Name: ).*(?= Track Type)'
    track_type_pattern = r'(?<=Track Type: ).*(?= Track)'

    race_info = race_details.find("td").text
    race["race_track"] = re.findall(track_name_pattern, race_info)[0]
    race["race_type"] = re.findall(track_type_pattern, race_info)[0]
    race["race_prize_pool"] = race_info.split(" ")[1].split(".")[0]
    return race

def extract_horse_result_details(result: BeautifulSoup):
    table_rows = result.find_all('tr')
    race_results = []
    for row in table_rows[1:]:
        horse = {}
        horse["scratched"] = "Scratched" in row["class"]
        table_data = row.find_all("td")

        horse["finished"] = table_data[1].text
        horse["started"] = table_data[7].text
        horse["margin"] = '0' if table_data[6].text == '' else table_data[6].text
        horse["weight"] = table_data[8].text
        horse["starting_price"] = table_data[10].text

        horse_data = row.find("td", class_ = "horse")
        horse["name_link"] = horse_data.find("a")['href']
        horse["code"] = horse_data.find("a")['href'].split("&")[0].split("=")[1]
        race_results.append(horse)
    return race_results

def impl_extract_race_details(result):
    details = result[0]
    results = result[1]

    race = extract_race_meta_details(details)
    #print(race)
    race["result"] = extract_horse_result_details(results)
    return(race)

def extract_race_details(url: str):
    page = requests.get(url, verify = False)
    soup = BeautifulSoup(page.content, "html.parser")
    ## race outcomes and details
    race_titles = soup.find_all("table", class_ = "race-title")
    race_results = soup.find_all("table", class_ = "race-strip-fields")

    results = list(zip(race_titles, race_results))
    details = []
    for result in results:
        details.append(impl_extract_race_details(result))
    return details

