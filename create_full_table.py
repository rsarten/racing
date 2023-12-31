import sys

import numpy as np
import pandas as pd

from src.export.connections import get_engine, get_connection

def create_full_table(password: str):
    engine = get_engine(password)
    conn = get_connection(password)

    with open('sql/all_tables.sql', 'r') as query:
        all_tables = pd.read_sql_query(query.read(), conn)

    print("table shape:", all_tables.shape)
    all_tables.to_csv("data/all_tables.csv", index=False)

if __name__ == "__main__":
    password = sys.argv[1]
    create_full_table(password)
