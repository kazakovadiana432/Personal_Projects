-- On-time reviewed orders for the two categories that passed the rate bar.
-- One row per category and seller. The seller is the one on the highest-priced item.

with latest_review as (
    select distinct on (order_id)
        order_id,
        review_score
    from reviews
    order by order_id, review_creation_date desc, review_answer_timestamp desc
),
top_item as (
    select distinct on (order_id)
        order_id,
        product_id,
        seller_id
    from items
    order by order_id, price desc, order_item_id
),
base as (
    select
        coalesce(
            cat.product_category_name_english,
            pr.product_category_name,
            'unknown'
        ) as category,
        i.seller_id,
        r.review_score,
        o.order_status = 'delivered'
            and o.order_delivered_customer_date is not null
            and o.order_estimated_delivery_date is not null
            and cast(o.order_delivered_customer_date as date)
                <= cast(o.order_estimated_delivery_date as date) as on_time
    from orders o
    join params p
        on o.order_purchase_timestamp >= p.monitor_start
       and o.order_purchase_timestamp < p.monitor_end
    join latest_review r using (order_id)
    join top_item i using (order_id)
    left join products pr using (product_id)
    left join categories cat
        on cat.product_category_name = pr.product_category_name
)
select
    category,
    seller_id,
    count(*) as on_time_reviewed,
    count(*) filter (where review_score in ({BAD_REVIEW_SCORES})) as on_time_bad
from base
where on_time
  and category in ('office_furniture', 'fixed_telephony')
group by category, seller_id
order by category, on_time_bad desc
