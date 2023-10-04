import sys
import numpy as np
import pandas as pd

## Generics

def get_id(query, conn):
    with conn.cursor() as cursor:
        cursor.execute(query)
        id = cursor.fetchone()
        if id is not None:
            id = id[0]
    return id

def add_entry(statement, values, conn):
    """
    Attempt to add entry using statement and values. Expects that
    statement will attempt to return PK value.
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(statement, values)
            id = cursor.fetchone()[0]
            conn.commit()
        except:
            id = None
            conn.rollback()
            print("error encountered")
    return id

## Get table IDs

def get_venue_id(state, venue, conn):
    id_query = f"""
    select venue_id from racing.venues where
    \"state\" = \'{state}\' and \"name\" = \'{venue}\';
    """
    return get_id(query=id_query, conn=conn)

def get_meet_id(venue_id, date, meet_type, conn):
    id_query = f"""
    select meet_id from racing.meets 
    where venue_id = {venue_id} 
    and \"date\" = \'{date}\'
    and meet_type = \'{meet_type}\';
    """
    return get_id(query=id_query, conn=conn)

def get_race_id(meet_id, race_number, conn):
    id_query = f"""
    select race_id from racing.races 
    where meet_id = {meet_id} 
    and race_number = {race_number};
    """
    return get_id(query=id_query, conn=conn)

def get_track_id(venue_id, distance, conn):
    id_query = f"""
    select track_id from racing.tracks 
    where venue_id = {venue_id} 
    and distance = {distance};
    """
    return get_id(query=id_query, conn=conn)

def get_result_id(race_id, horse_id, conn):
    id_query = f"""
    select result_id from racing.results 
    where race_id = {race_id} 
    and horse_id = {horse_id};
    """
    return get_id(query=id_query, conn=conn)

def get_horse_id(horse_code, conn):
    id_query = f"""
    select horse_id from racing.horses where
    horse_code = \'{horse_code}\';
    """
    return get_id(query=id_query, conn=conn)

def get_jockey_id(jockey_code, conn):
    id_query = f"""
    select jockey_id from racing.jockeys where
    jockey_code = \'{jockey_code}\';
    """
    return get_id(query=id_query, conn=conn)

def get_trainer_id(trainer_code, conn):
    id_query = f"""
    select trainer_id from racing.trainers where
    trainer_code = \'{trainer_code}\';
    """
    return get_id(query=id_query, conn=conn)

def get_venue_from_meet(meet_id, conn):
    id_query = f"""
    select venue_id from racing.meets where
    meet_id = {meet_id};
    """
    return get_id(query=id_query, conn=conn)

## Check and add table rows

def add_venue(state, venue, conn):
    venue_id = get_venue_id(state, venue, conn)
    if venue_id is None:
        statement = """
        insert into racing.venues(state, name)
        values (%s, %s) returning venue_id
        """
        values = (state, venue)
        venue_id = add_entry(statement, values, conn)
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
