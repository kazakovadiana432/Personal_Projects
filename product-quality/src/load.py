"""load the raw CSVs into the database"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.paths import RAW_DIR, SQL_DIR
from config.settings import BAD_REVIEW_SCORES, MONITOR_END, MONITOR_START

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "categories": "product_category_name_translation.csv",
}


def attach(con):
    for view, filename in TABLES.items():
        path = (RAW_DIR / filename).as_posix()
        con.sql(
            f"create or replace view {view} as "
            f"select * from read_csv('{path}', header=true, auto_detect=true)"
        )

def add_window(con):
    con.sql(
        f"""
        create or replace view params as
        select timestamp '{MONITOR_START}' as monitor_start,
               timestamp '{MONITOR_END}' as monitor_end
        """
    )

def run_sql(con, filename):
    sql = (SQL_DIR / filename).read_text(encoding="utf-8")
    scores = ", ".join(str(int(score)) for score in BAD_REVIEW_SCORES)
    sql = sql.replace("{BAD_REVIEW_SCORES}", scores)
    return con.sql(sql).df()
