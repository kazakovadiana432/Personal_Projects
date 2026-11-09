"""Analysis of seller influence on the on-time bad-review rate"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import duckdb

from config.settings import MIN_ON_TIME_GAP, MIN_TOP_SELLER_SHARE
from src.load import add_window, attach, run_sql


def main():
    con = duckdb.connect()
    attach(con)
    add_window(con)
    sellers = run_sql(con, "seller_check.sql")
    counts = run_sql(con, "category_rates.sql")
    overall_on_time = counts["on_time_bad"].sum() / counts["on_time_reviewed"].sum()

    for category, rows in sellers.groupby("category", sort=True):
        reviewed = int(rows["on_time_reviewed"].sum())
        bad = int(rows["on_time_bad"].sum())
        top = rows.sort_values("on_time_bad", ascending=False).iloc[0]
        others = rows.loc[rows["seller_id"] != top.seller_id]
        other_reviewed = int(others["on_time_reviewed"].sum())
        other_bad = int(others["on_time_bad"].sum())
        other_rate = other_bad / other_reviewed
        bad_share = top.on_time_bad / bad
        order_share = top.on_time_reviewed / reviewed
        print(category)
        print(f"  sellers: {len(rows)}")
        print(f"  on-time reviews: {reviewed}")
        print(f"  on-time bad reviews: {bad}")
        print(f"  biggest seller: {top.seller_id}")
        print(f"  biggest seller share of bad reviews: {bad_share:.4f}")
        print(f"  biggest seller share of on-time orders: {order_share:.4f}")
        print(f"  one seller: {bad_share >= MIN_TOP_SELLER_SHARE}")
        print(f"  other sellers on-time rate: {other_rate:.4f}")
        print(f"  other sellers gap: {other_rate - overall_on_time:.4f}")
        print(f"  other sellers still pass: {other_rate - overall_on_time >= MIN_ON_TIME_GAP}")
        print()


if __name__ == "__main__":
    main()
