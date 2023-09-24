import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_meet_details, extract_race_details
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection

engine = get_engine(password)
conn = get_connection(password)

meet_links = pd.read_sql_query("select meet_id, link from racing.meets", engine)