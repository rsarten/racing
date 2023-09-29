import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_meet_details, extract_race_details
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.model.structs import Venue, Meet, Track, Race, Result, Horse, Jockey, Trainer

password="Dictionary1"
engine = get_engine(password)
conn = get_connection(password)

meet_links = pd.read_sql_query("select * from racing.meets", engine)

meets = meet_links.to_dict(orient="records")
meet1 = meets[0]

meet1["details"] = extract_race_details(meet1["link"])
meet = Meet(**meet1)

m = meets[0]

m1 = Meet(**m)


def extract_races(meet: Meet) -> Meet:
    page = requests.get(meet.link, verify = False)
    soup = BeautifulSoup(page.content, "html.parser")

    race_titles = soup.find_all("table", class_ = "race-title")
    race_results = soup.find_all("table", class_ = "race-strip-fields")
    races = list(zip(race_titles, race_results))
    for race in races:
        meet.races.append(extract_race(race))
    return meet

race = races[0]

def extract_race(race):
    details = race[0]
    results = race[1]

    race_ = Race(**extract_race_info(details))
    race_.results = extract_race_results(results)
    race_["result"] = extract_horse_result_details(results)
    return(race)
