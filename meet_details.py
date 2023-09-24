import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_meet_details, extract_race_details
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.model.structs import Venue, Meet, Track, Race, Result, Horse

password=
engine = get_engine(password)
conn = get_connection(password)

meet_links = pd.read_sql_query("select * from racing.meets", engine)

meets = meet_links.to_dict(orient="records")

m = meets[0]

m1 = Meet(**m)
m1.retrieve_id(conn)

m1.add_to_db(conn)

