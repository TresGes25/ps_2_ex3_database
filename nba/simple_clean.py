import sqlite3 as sql
import pandas as pd
from pathlib import Path


def simple_clean(query: str) -> pd.DataFrame:
    """
    This function establishes a connection to the path
    and executes the query. It then performs basic cleans.
    """
    data_path = Path.cwd() / "data" / "nba.sqlite"
    con = sql.connect(data_path)
    df = pd.read_sql(query, con)
    # Strip column names and reset index
    df.columns = df.columns.str.strip()
    df = df.reset_index(drop=True)
    return df
