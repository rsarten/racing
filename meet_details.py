import numpy as np
import pandas as pd

from src.scrape.extract_records import extract_races
from src.scrape.utils import date_from_link, clean_venue

from src.export.connections import get_engine, get_connection
from src.export.table_work import add_entry
from src.model.structs import Meet

password=""
engine = get_engine(password)
conn = get_connection(password)

meet_links = pd.read_sql_query("select * from racing.meets where \"status\" is null", engine)
meet_links.drop("status", axis=1, inplace=True)

meets = meet_links.to_dict(orient="records")

def store_meet(meet : Meet, conn):
    status = f"writing {meet.meet_id}"
    if not bool(meet.races):
        return "no races" 
    try:
        meet.id_to_children()
        status = "handling races"
        for i, race in enumerate(meet.races):
            status = f"handle race {i}"
            race.track.add_to_db(conn)
            race.add_to_db(conn, cascade=False)
            race.id_to_children()

        status = "handling results"
        for i, race in enumerate(meet.races):
            for j, result in enumerate(race.results):
                status = f"handle race {i}, result {j}"
                result.id_to_children(conn)
                result.add_to_db(conn)
    except:
        with open('data/scrape_write_errors', 'a') as f:
            f.write(f'{meet.meet_id},"{status}"\n')
        return status
    return "success"

for i, meet in enumerate(meets):
    meet_id = meet["meet_id"]
    print(i)
    status = "create meet"
    try:
        meet = Meet(**meet)
        status = "scrape meet"
        meet = extract_races(meet)
        status = store_meet(meet, conn)
    except:
        with open('data/scrape_write_errors', 'a') as f:
            f.write(f'{meet_id},"{status}"\n')
    
    if status != "success" and status != "no races":
        status = "error: " + status

    add_entry(
        """
        update racing.meets
        set "status" = %s
        where meet_id = %s
        returning meet_id
        """,
        (status, meet_id),
        conn)
    print(status)
    print("----------------")


conn.close()
engine.dispose()

