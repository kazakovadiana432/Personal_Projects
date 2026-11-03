-- Counts that fix the grain of the later rates. No window is applied.

select 'orders' as check_name, count(*) as n
from orders
union all
select 'orders with more than one review' as check_name, count(*) as n 
from (
    select order_id
    from reviews
    group by 1
    having count(*) > 1
)
union all
select 'review_id used on more than one order' as check_name, count(*) as n
from (select review_id from reviews group by 1 having count(distinct order_id) > 1)
union all
select 'multi-review orders whose scores disagree' as check_name, count(*) as n
from (select order_id from reviews group by 1 having count(*) > 1 and count(distinct review_score) > 1)
union all
select 'orders with more than one item' as check_name, count(*) as n
from (
    select order_id
    from items
    group by 1
    having count(*) > 1
)
union all
select 'orders with no review' as check_name, count(*) as n
from orders o
where not exists (
    select 1 from reviews r where r.order_id = o.order_id
)

union all
select 'orders with no items' as check_name, count(*) as n
from orders o
left join items i using (order_id)
where i.order_id is null

union all
select 'orders with more than one item' as check_name, count(*) as n
from (
    select order_id
    from items
    group by 1
    having count(*) > 1
)

union all
select 'products with no category' as check_name, count(*) as n
from products
where product_category_name is null

union all
select 'category names with no English translation' as check_name, count(*) as n
from products
where product_category_name is not null
  and product_category_name not in (select product_category_name from categories)
