# Product quality on Olist orders

This is an analysis of real Olist orders, a Brazilian marketplace, from the [public Kaggle extract](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
The question is which product categories are more prone to a bad review, and whether that is still true when the order arrived on time.
A bad review is a latest score of 1 or 2.
The review is on the order, not on a product. The category is the highest-priced item.
Thresholds are locked in `config/settings.py` before the chart.
A category is flagged if it has at least 200 orders and its on-time bad-review rate is 5 pp or more above the overall on-time rate.
A flagged category is treated as one seller if that seller has at least half of its on-time bad reviews.

## Where to start

1. `docs/product_question.md` defines the question and the pre-committed thresholds.
2. `config/settings.py` holds the rate thresholds and, after the quality check, the window dates.
3. `notebooks/findings.ipynb` prints each step, the window chosen from the month counts, and the conclusion.

File locations are in `config/paths.py`.

## How to run

From the project root, with the project venv:

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt

python src/quality.py
python src/category_rates.py
python src/seller_check.py
```

`.venv` points at `C:\Users\926613\venvs\product-quality`. A venv created inside this OneDrive path hits the Windows path limit.
If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same window.
The notebook kernel is this venv, not another project's.

`quality.py` prints orders by purchase month, and the review and item counts, before any window is applied.
`category_rates.py` prints the bad-review rate by category and saves the on-time chart.
`seller_check.py` is only for the categories that were flagged. It prints whether one seller holds the bad reviews.

## Layout

```
config/     thresholds and file paths
sql/        one query per step
src/        load the CSVs, data quality, category rates, seller check
docs/       the question
notebooks/  step-by-step run, the window decision, and the conclusion
data/raw/   Olist CSVs
```

The queries use orders, items, reviews, products, and the category translation.
Payments, customers, the sellers lookup, and geolocation are in `data/raw` and are not used. The seller id comes from the item row.

## Outputs

| File | From |
|---|---|
| `data/category_on_time.png` | `category_rates.py` |

The rate table and the seller check print to the terminal. The same numbers are in `notebooks/findings.ipynb`.

## Result

Across the window, the on-time bad-review rate is 9.3%.
Office furniture is flagged at 18.2% on time, 9.0 pp above that rate. One seller has 78.3% of that category's on-time bad reviews. Without that seller the category rate is 13.3%, 4.1 pp above the overall rate, so the category itself is not flagged.
Fixed telephony is flagged at 14.4% on time (28 of 195 reviews) and is not one seller. A 95% Wilson interval for that rate is 10.1% to 20.0%.
Review the office furniture seller. Monitor fixed telephony until there are more reviews.

## Limits

- The purchase window is January 2017 through August 2018, chosen after the month counts in the quality step. The end date is excluded. Months outside the window are partial and excluded.
- A missing review is left out of the bad-review rate. It is not counted as a good review.
- On time means delivered, with both dates, and the delivery date is not after the estimate.
- The score is the whole order, given to the highest-priced item. It does not say a product is defective.
- The sellers file has an id and no seller name.
