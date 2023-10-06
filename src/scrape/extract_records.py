import numpy as np
import pandas as pd

import re
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from bs4 import BeautifulSoup

from src.model.structs import Venue, Meet, Track, Race, Result, Horse, Jockey, Trainer
from src.scrape.utils import int_or_0, float_or_0
from src.scrape.utils import date_from_link, clean_venue

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

def meet_overview(meet: BeautifulSoup) -> dict:
    tds = meet.find_all("td")
    meet_link = tds[1].find("a")['href']
    meet_desc = tds[1].text.split(" - ") # 1st part venue, 2nd part type

    meet_data = {
        "date": date_from_link(meet_link).strip(),
        "venue": clean_venue(meet_desc[0]).strip(),
        "meet_type": meet_desc[1].split("(")[0].strip(),
        "link": site + meet_link
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

def extract_race_info(race_details: BeautifulSoup):
    details = race_details.find("th").text.split('\r')[0]
    race_info = {
        "race_number": int(re.findall(r'(?<=^Race )\d*', details)[0]),
        "race_time": re.findall(r'[\d:AP]+M', details)[0]
    }
    info = race_details.find("td").text
    race_info["prize_pool"] = info.split(" ")[1].split(".")[0].strip("$").replace(",", "")
    race_info["winning_time"] = re.findall(r'(?<=Time: )[\d:\.]*', info)[0]
    return race_info

def extract_track(race_details: BeautifulSoup) -> Track:
    details = race_details.find("th").text.split('\r')[0]
    distance= int(re.findall(r'(?<=\()\d+(?= METRES)', details)[0])

    race_info = race_details.find("td").text
    track_type = re.findall(r'(?<=Track Type: ).*(?= Track)', race_info)[0]

    track = Track(distance=distance, track_type=track_type)
    return track

def extract_horse(result_row: BeautifulSoup) -> Horse:
    horse_data = result_row.find("td", class_ = "horse")
    horse_link = horse_data.find("a")['href']
    return Horse(horse_name= horse_data.text.strip(),
                 horse_code= re.findall(r'(?<=horsecode=).*(?=&stage)', horse_link)[0])

def extract_jockey(result_row: BeautifulSoup) -> Jockey:
    jockey_data = result_row.find("td", class_ = "jockey")
    jockey_link = jockey_data.find("a")['href']
    return Jockey(jockey_name= jockey_data.text.strip(),
                  jockey_code= re.findall(r'(?<=jockeycode=).*', jockey_link)[0].strip())

def extract_trainer(result_row: BeautifulSoup) -> Trainer:
    trainer_data = result_row.find("td", class_ = "trainer")
    trainer_link = trainer_data.find("a")['href']
    return Trainer(trainer_name= trainer_data.text.strip(),
                   trainer_code= re.findall(r'(?<=trainercode=).*(?=&trainer)', trainer_link)[0].strip())

def extract_result(result_row: BeautifulSoup) -> Result:
    row_data = result_row.find_all("td")
    result = Result(finished= int_or_0(row_data[1].text.strip()),
                    margin= float_or_0(row_data[6].text.strip("L")),
                    barrier= int_or_0(row_data[7].text),
                    scratched= "Scratched" in result_row["class"],
                    starting_price= float_or_0(row_data[10].text.strip("$").strip("F").strip("E")),
                    weight= float_or_0(row_data[8].text.split(" ")[0].strip("kg")),
                    horse= extract_horse(result_row),
                    jockey= extract_jockey(result_row),
                    trainer= extract_trainer(result_row))
    return result
        
def extract_race_results(results: BeautifulSoup) -> [Result]:
    # omit first row, as only header info
    # for i, row in enumerate(results.find_all('tr')[1:]):
    #     print(i)
    #     extract_result(row)
    return [extract_result(row) for row in results.find_all('tr')[1:]]

def extract_race(race_: tuple) -> [Race]:
    details = race_[0]
    results = race_[1]

    race = Race(**extract_race_info(details))
    race.results = extract_race_results(results)
    race.track = extract_track(details)
    return(race)

def extract_races(meet: Meet) -> Meet:
    page = requests.get(meet.link, verify = False)
    soup = BeautifulSoup(page.content, "html.parser")

    race_titles = soup.find_all("table", class_ = "race-title")
    race_results = soup.find_all("table", class_ = "race-strip-fields")
    races = list(zip(race_titles, race_results))
    # for i, race in enumerate(races):
    #     print(i)
    #     extract_race(race)
    meet.races = [extract_race(race) for race in races]
    return meet