import sys
import numpy as np
import pandas as pd

def get_venue_id(state, venue, conn):
    with conn.cursor() as cursor:
        cursor.execute(f"""select venue_id from racing.venues where
                        \"state\" = \'{state}\' and \"name\" = \'{venue}\';""")
        venue_id = cursor.fetchone()
        if venue_id is not None:
            venue_id = venue_id[0]
    return venue_id

def add_venue(state, venue, conn, engine):
    venue_id = get_venue_id(state, venue, conn)
    if venue_id is None:
        venue_df = pd.DataFrame({"state": [state], "name": [venue]})
        venue_df.to_sql("venues", engine, index=False, if_exists="append", schema="racing")
        venue_id = get_venue_id(state, venue, conn)
    return venue_id