"""Bad-review rate by category, and the same rate among on-time orders.

Ranking on the raw bad-review rate mixes late delivery into product quality.
The locked rule uses the on-time gap.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import duckdb
import matplotlib.pyplot as plt

from config.paths import CATEGORY_CHART
from config.settings import MIN_CATEGORY_ORDERS, MIN_ON_TIME_GAP
from src.load import add_window, attach, run_sql


def main():
    con = duckdb.connect()
    attach(con)
    add_window(con)
    counts = run_sql(con, "category_rates.sql")

    orders = int(counts["orders"].sum())
    reviewed = int(counts["reviewed"].sum())
    bad = int(counts["bad"].sum())
    delivered = int(counts["delivered"].sum())
    late = int(counts["late"].sum())
    on_time_reviewed = int(counts["on_time_reviewed"].sum())
    on_time_bad = int(counts["on_time_bad"].sum())
    overall_on_time = on_time_bad / on_time_reviewed

    ranked = counts.loc[counts["orders"] >= MIN_CATEGORY_ORDERS].copy()
    ranked["bad_review_rate"] = ranked["bad"] / ranked["reviewed"]
    ranked["late_share"] = ranked["late"] / ranked["delivered"]
    ranked["on_time_rate"] = ranked["on_time_bad"] / ranked["on_time_reviewed"]
    ranked["on_time_gap"] = ranked["on_time_rate"] - overall_on_time
    ranked["passes"] = ranked["on_time_gap"] >= MIN_ON_TIME_GAP
    ranked = ranked.sort_values("on_time_gap", ascending=False)

    small = int((counts["orders"] < MIN_CATEGORY_ORDERS).sum())

    print(f"orders: {orders}")
    print(f"bad-review rate: {bad / reviewed:.4f}")
    print(f"late share: {late / delivered:.4f}")
    print(f"on-time bad-review rate: {overall_on_time:.4f}")
    print(f"categories under {MIN_CATEGORY_ORDERS} orders: {small}")
    print()
    show = ranked[
        [
            "category",
            "orders",
            "bad_review_rate",
            "late_share",
            "on_time_reviewed",
            "on_time_rate",
            "on_time_gap",
            "passes",
        ]
    ]
    print(show.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print()
    passed = ranked.loc[ranked["passes"], "category"].tolist()
    print(f"pass the {MIN_ON_TIME_GAP:.0%} on-time bar: {passed if passed else 'none'}")

    chart(ranked, overall_on_time)


def chart(ranked, overall_on_time):
    plot = ranked.sort_values("on_time_rate")
    fig, ax = plt.subplots(figsize=(8, max(4, 0.28 * len(plot))))
    ax.barh(plot["category"], plot["on_time_rate"], color="0.45")
    ax.axvline(overall_on_time, color="black", linewidth=1, label="all on-time orders")
    ax.axvline(
        overall_on_time + MIN_ON_TIME_GAP,
        color="black",
        linewidth=1,
        linestyle="--",
        label="5 point bar",
    )
    ax.set_xlabel("bad-review rate, on-time orders")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CATEGORY_CHART, dpi=100)
    plt.close()


if __name__ == "__main__":
    main()
