-- One row per category. We keep the latest review for each order. Category is the highest-priced item.

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
        product_id
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
        r.review_score,
        o.order_status = 'delivered'
            and o.order_delivered_customer_date is not null
            and o.order_estimated_delivery_date is not null as is_delivered,
        cast(o.order_delivered_customer_date as date)
            > cast(o.order_estimated_delivery_date as date) as after_estimate
    from orders o
    inner join params p
        on o.order_purchase_timestamp >= p.monitor_start
       and o.order_purchase_timestamp < p.monitor_end
    left join latest_review r using (order_id)
    left join top_item i using (order_id)
    left join products pr using (product_id)
    left join categories cat
        on cat.product_category_name = pr.product_category_name
)
select
    category,
    count(*) as orders,
    count(review_score) as reviewed,
    count(*) filter (where review_score in ({BAD_REVIEW_SCORES})) as bad,
    count(*) filter (where is_delivered) as delivered,
    count(*) filter (where is_delivered and after_estimate) as late,
    count(*) filter (
        where is_delivered and not after_estimate and review_score is not null
    ) as on_time_reviewed,
    count(*) filter (
        where is_delivered
          and not after_estimate
          and review_score in ({BAD_REVIEW_SCORES})
    ) as on_time_bad
from base
group by category
order by orders desc
