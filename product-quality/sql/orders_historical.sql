-- One row per purchase month, from the first month in the file to the last.
-- A month with no orders is 0

with months as (
    select
        strftime(order_purchase_timestamp, '%Y-%m') as month,
        count(*) as orders
    from orders
    group by 1
),
bounds as (
    select
        strftime(min(order_purchase_timestamp), '%Y-%m') as start_month,
        strftime(max(order_purchase_timestamp), '%Y-%m') as end_month
    from orders
),
spine as (
    select strftime(month_start, '%Y-%m') as month
    from bounds,
        generate_series(
            strptime(start_month || '-01', '%Y-%m-%d'),
            strptime(end_month || '-01', '%Y-%m-%d'),
            interval 1 month
        ) as t(month_start)
)
select
    spine.month,
    coalesce(months.orders, 0) as orders
from spine
left join months using (month)
order by spine.month
