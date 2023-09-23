import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import time

from src.export.connections import get_engine, get_connection
from src.export.table_work import add_meet

meets = pd.read_csv("data/meet_links.csv", index_col=False)
meets["meet_type"] = "Professional"
meets = meets.to_dict(orient = "records")
meets[0]

#password =
engine = get_engine(password)
conn = get_connection(password)

add_meet(meets[0], conn, engine)

status = []
for meet in meets:
    result = add_meet(meet, conn, engine)
    print(result)
    status.append(result)

engine.dispose()
conn.close()