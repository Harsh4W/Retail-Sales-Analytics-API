SELECT
    COUNT(*) AS total_customers
FROM customers;
SELECT
    COUNT(*) AS total_orders
FROM orders;
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
SELECT
    ROUND(SUM(price), 2) AS total_product_sales
FROM order_items;
SELECT
    ROUND(SUM(price + freight_value), 2)
        AS total_sales_including_freight
FROM order_items;
SELECT
    strftime(
        '%Y-%m',
        o.order_purchase_timestamp
    ) AS sales_month,

    ROUND(SUM(oi.price), 2) AS monthly_product_sales

FROM orders o

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY sales_month

ORDER BY sales_month;
SELECT
    p.product_id,

    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS product_category,

    COUNT(*) AS order_lines,

    ROUND(SUM(oi.price), 2) AS total_product_sales

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation t
    ON p.product_category_name =
       t.product_category_name

JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    p.product_id,
    product_category

ORDER BY total_product_sales DESC

LIMIT 10;
SELECT
    COALESCE(
        t.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category,

    COUNT(*) AS order_lines,

    ROUND(SUM(oi.price), 2) AS total_product_sales

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation t
    ON p.product_category_name =
       t.product_category_name

JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_status = 'delivered'

GROUP BY category

ORDER BY total_product_sales DESC

LIMIT 10;
WITH order_sales AS (

    SELECT
        order_id,
        SUM(price) AS product_sales

    FROM order_items

    GROUP BY order_id

)

SELECT
    c.customer_unique_id,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(SUM(os.product_sales), 2) AS total_product_sales

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN order_sales os
    ON o.order_id = os.order_id

WHERE o.order_status = 'delivered'

GROUP BY c.customer_unique_id

ORDER BY total_product_sales DESC

LIMIT 10;
SELECT
    c.customer_state,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(SUM(oi.price), 2) AS total_product_sales

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'delivered'

GROUP BY c.customer_state

ORDER BY total_product_sales DESC;
SELECT
    payment_type,

    COUNT(*) AS payment_records,

    COUNT(DISTINCT order_id) AS unique_orders,

    ROUND(SUM(payment_value), 2) AS total_payment_value

FROM order_payments

GROUP BY payment_type

ORDER BY total_payment_value DESC;
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score,

    COUNT(*) AS total_review_records

FROM order_reviews;
SELECT

    COUNT(*) AS delivered_orders,

    ROUND(
        AVG(
            julianday(order_delivered_customer_date) -
            julianday(order_purchase_timestamp)
        ),
        2
    ) AS average_delivery_days,

    ROUND(
        AVG(
            julianday(order_delivered_customer_date) -
            julianday(order_estimated_delivery_date)
        ),
        2
    ) AS average_days_vs_estimate

FROM orders

WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_purchase_timestamp IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL;
SELECT

    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN order_status = 'canceled'
            THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_status = 'canceled'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS cancellation_percentage

FROM orders;

