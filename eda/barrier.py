import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links

from src.export.connections import get_engine, get_connection
from src.model.structs import Meet
from src.export.table_work import add_venue

password=
engine = get_engine(password)
conn = get_connection(password)

barrier_query = """
with
meets as (
	select
		venue_id,
		meet_id
	from racing.meets
),

races as (
	select
		race_id,
		meet_id,
		track_id
	from racing.races
),

tracks as (
	select
		track_id,
		distance
	from racing.tracks
),

results as (
	select
		race_id,
		barrier,
		finished,
		margin
	from racing.results
)

select *
from races as r
left join tracks as t
	using(track_id)
left join results as res
	using(race_id)
left join meets as me
	using(meet_id);
"""

barriers = pd.read_sql_query(barrier_query, engine)
barriers.to_csv("data/barriers.csv", index=False)

randwick = pd.read_sql_query("select * from racing.meets where venue_id = 50", engine)
randwick.meet_id
