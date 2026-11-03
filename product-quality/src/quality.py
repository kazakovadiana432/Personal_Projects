"""Check the quality of the data"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import duckdb

from src.load import attach, run_sql


def main():
    con = duckdb.connect()
    attach(con)
    print("EDA of the data")
    print(run_sql(con, "quality_values.sql").to_string(index=False))
    print()
    print("quality analysis by grain")
    print(run_sql(con, "quality_grain.sql").to_string(index=False))


if __name__ == "__main__":
    main()
