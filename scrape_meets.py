import numpy as np
import pandas as pd

from src.scrape.extract_records import meet_links

from src.export.connections import get_engine, get_connection
from src.model.structs import Meet
from src.export.table_work import add_venue

password=
conn = get_connection(password)

new_meets = meet_links()
new_meets = new_meets.to_dict(orient="records")

with conn.cursor() as cursor:
    cursor.execute("select max(meet_id) from racing.meets")
    current_meets_count = cursor.fetchone()[0]

for meet in new_meets:
    meet["venue_id"] = add_venue(meet["state"], meet["venue"], conn)
    m = {
        "venue_id": meet["venue_id"],
        "date": meet["date"],
        "link": meet["link"],
        "meet_type": meet["meet_type"]
    }
    meet = (Meet(**m))
    meet.add_to_db(conn, cascade = False)

with conn.cursor() as cursor:
    cursor.execute("select max(meet_id) from racing.meets")
    new_meets_count = cursor.fetchone()[0]

print("prev meet count", current_meets_count)
print("new meet count", new_meets_count)
print("new meets: ", new_meets_count - current_meets_count)

conn.close()
