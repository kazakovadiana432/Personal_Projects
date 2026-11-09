"""Analysis of seller influence on the on-time bad-review rate"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import duckdb

from src.load import add_window, attach, run_sql


def main():
    con = duckdb.connect()
    attach(con)
    add_window(con)
    sellers = run_sql(con, "seller_check.sql")
    counts = run_sql(con, "category_rates.sql")

if __name__ == "__main__":
    main()
