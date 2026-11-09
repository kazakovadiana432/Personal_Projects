-- Nulls, duplicate keys, and values off the scale the rates use. No window.

select 'null review_score' as check_name, count(*) as n
from reviews
where review_score is null
union all
select 'null purchase timestamp', count(*)
from orders
where order_purchase_timestamp is null
union all
select 'null order_status', count(*)
from orders
where order_status is null
union all
select 'null delivered date', count(*)
from orders
where order_delivered_customer_date is null
union all
select 'null estimated delivery date', count(*)
from orders
where order_estimated_delivery_date is null
union all
select 'null price', count(*)
from items
where price is null
union all
select 'null product category', count(*)
from products
where product_category_name is null
union all
select 'duplicate order_id', count(*)
from (
    select order_id from orders group by 1 having count(*) > 1
)
union all
select 'duplicate review_id', count(*)
from (
    select review_id from reviews group by 1 having count(*) > 1
)
union all
select 'duplicate order item', count(*)
from (
    select order_id, order_item_id
    from items
    group by 1, 2
    having count(*) > 1
)
union all
select 'review_score outside 1-5', count(*)
from reviews
where review_score is not null
  and review_score not in (1, 2, 3, 4, 5)
union all
select 'price at or below 0', count(*)
from items
where price <= 0
union all
select 'delivered before purchase', count(*)
from orders
where order_delivered_customer_date is not null
  and order_purchase_timestamp is not null
  and order_delivered_customer_date < order_purchase_timestamp
