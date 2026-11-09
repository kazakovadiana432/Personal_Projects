"""
Bars for the category question. Locked before the chart.
"""

SEED = 42

# Bad review: score 1 or 2. Score 3 is lukewarm, not a failure.
BAD_REVIEW_SCORES = (1, 2)

# A category under this many orders is too small to rank.
MIN_CATEGORY_ORDERS = 200

# On-time bad-review rate, category minus all orders.
# Same 5 point bar as "large enough to care."
MIN_ON_TIME_GAP = 0.05

# Purchase window. End is excluded. Outside it the months are scraps.
MONITOR_START = "2017-01-01"
MONITOR_END = "2018-09-01"

# One seller has most of the on-time bad reviews.
MIN_TOP_SELLER_SHARE = 0.50