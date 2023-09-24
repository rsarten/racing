import sys
import numpy as np
import pandas as pd

def get_id(query, conn):
    with conn.cursor() as cursor:
        cursor.execute(query)
        id = cursor.fetchone()
        if id is not None:
            id = id[0]
    return id

def get_venue_id(state, venue, conn):
    id_query = f"""
    select venue_id from racing.venues where
    \"state\" = \'{state}\' and \"name\" = \'{venue}\';
    """
    return get_id(query=id_query, conn=conn)

def get_horse_id(horse_code, conn):
    id_query = f"""
    select horse_id from racing.horses where
    horse_code = \'{horse_code}\';
    """
    return get_id(query=id_query, conn=conn)


def add_venue(state, venue, conn, engine):
    venue_id = get_venue_id(state, venue, conn)
    if venue_id is None:
        venue_df = pd.DataFrame({"state": [state], "name": [venue]})
        venue_df.to_sql("venues", engine, index=False, if_exists="append", schema="racing")
        venue_id = get_venue_id(state, venue, conn)
    return venue_id

def add_meet(meet, conn, engine):
    venue_id = add_venue(meet["state"], meet["venue"], conn, engine)

    with conn.cursor() as cursor:
        cursor.execute(f"""select meet_id from racing.meets 
                       where venue_id = {venue_id} 
                       and \"date\" = \'{meet["date"]}\'
                       and meet_type = \'{meet["meet_type"]}\';""")
        meet_id = cursor.fetchone()
    if meet_id is not None:
        print("meet:", meet["venue"], meet["date"], "already exists")
        return("already present")
    meet_df = pd.DataFrame({"venue_id": [venue_id],
                            "date": [meet["date"]],
                            "meet_type": [meet["meet_type"]],
                            "link": meet["link"]})
    meet_df.to_sql("meets", engine, index=False, if_exists="append", schema="racing")
    return "added"
