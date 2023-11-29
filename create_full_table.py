import numpy as np
import pandas as pd

from src.export.connections import get_engine, get_connection

password=""
engine = get_engine(password)
conn = get_connection(password)

with open('sql/all_tables.sql', 'r') as query:
    all_tables = pd.read_sql_query(query.read(), conn)

all_tables.to_csv("data/all_tables.csv", index=False)