import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links, extract_races
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.export.table_work import add_venue, add_entry
from src.model.structs import Meet

password=
engine = get_engine(password)
conn = get_connection(password)

meets = pd.read_sql_query("select * from racing.meets where \"status\" <> 'success' and \"status\" <> 'no races'", engine)
meets.value_counts("status")

meets = meets.to_dict(orient="records")
meet = meets[1]
meet["status"]
del meet["status"]

meet = Meet(**meet)
meet = extract_races(meet)
