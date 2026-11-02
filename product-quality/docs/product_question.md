## Product question

Which product categories are more prone to a bad review, and is that still true when the order arrived on time?

## Decision this changes

Which categories are a product problem, and which only look bad because more of their orders are late.

A bad review is a latest score of 1 or 2 on the order. The review is not tied to a product. The category is the highest-priced item on the order.

## Rule (pre-committed)

Bars are locked in [config/settings.py](../config/settings.py).

| Check | Pass if | Why |
|---|---|
| Enough orders | The category has at least 200 orders in the window | A category under 200 orders is too small to rank |
| Worse when on time | Bad-review rate among its on-time orders is at least 5 percentage points above the on-time rate for all orders | A category that fails this check is a delivery pattern, not a product-quality finding |