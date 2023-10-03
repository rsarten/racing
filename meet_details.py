import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_meet_details, extract_races
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.model.structs import Meet

password=
engine = get_engine(password)
conn = get_connection(password)

meet_links = pd.read_sql_query("select * from racing.meets", engine)

meets = meet_links.to_dict(orient="records")

def store_meet(meet, conn):
    try:
        meet.id_to_children()
        for race in meet.races:
            race.track.add_to_db(conn)
            race.add_to_db(conn, cascade=False)
            race.id_to_children()

            for result in race.results:
                result.id_to_children(conn)
                result.add_to_db(conn)
    except:
        with open('data/store_meet_errors', 'a') as f:
            f.write(f'{meet.meet_id},{meet.venue_id}\n')


for i, meet in enumerate(meets):
    print(i)
    meet = Meet(**meet)
    meet = extract_races(meet)
    store_meet(meet, conn)

