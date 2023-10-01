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

m = meets[0]

meet = Meet(**m)
meet = extract_races(meet)
meet.add_to_db(conn, cascade=True)
meet.venue_id
meet.races[0].add_to_db(conn)
race0 = meet.races[0]
race0.race_id is None
race0.meet_id
race0.race_number
race0.prize_pool
race0.track
type(race0)
"""
insert into racing.race(meet_id, track_id, race_number, prize_pool, time)
            values (%s, %s, %s, %s, %s) returning race_id
            """.format(
            race0.meet_id, 
            race0.track.track_id, 
            race0.race_number, 
            race0.prize_pool, 
            race0.time)
race0.retrieve_id(conn)


Meet.add_to_db(conn)