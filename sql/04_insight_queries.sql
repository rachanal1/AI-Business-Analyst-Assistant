-- ============================================================
-- 04_insight_queries.sql
-- AI Business Analyst Assistant
-- Purpose:
-- Perform advanced business analysis using CTEs,
-- LAG(), RANK(), EXTRACT(), CASE expressions,
-- and comparison with averages.
-- ============================================================


-- Insight 1:
-- Find the top 10 customers based on total revenue generated.
WITH customer_revenue AS (
    SELECT
        c.customer_unique_id,
        SUM(oi.price) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_unique_id
)
SELECT
    customer_unique_id,
    ROUND(total_revenue, 2) AS total_revenue
FROM customer_revenue
ORDER BY total_revenue DESC
LIMIT 10;


-- Insight 2:
-- Calculate revenue for each month
-- and rank the months by revenue.
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue
FROM monthly_revenue
ORDER BY revenue DESC;


-- Insight 3:
-- Find the month with the highest revenue.
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue
FROM monthly_revenue
ORDER BY revenue DESC
LIMIT 1;


-- Insight 4:
-- Compare each month's revenue with
-- the previous month's revenue using LAG().
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        LAG(revenue) OVER (ORDER BY month),
        2
    ) AS previous_month_revenue
FROM monthly_revenue
ORDER BY month;


-- Insight 5:
-- Calculate month-over-month revenue growth percentage.
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
),
revenue_with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        100.0 * (revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS mom_growth_percentage
FROM revenue_with_previous
ORDER BY month;


-- Insight 6:
-- Rank product categories by revenue.
-- RANK() gives the same rank to categories with tied revenue.
WITH category_revenue AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM category_revenue
ORDER BY revenue_rank;


-- Insight 7:
-- Classify customer reviews into Poor, Neutral,
-- and Good categories based on review score.
SELECT
    review_score,
    CASE
        WHEN review_score <= 2 THEN 'Poor'
        WHEN review_score = 3 THEN 'Neutral'
        WHEN review_score >= 4 THEN 'Good'
    END AS review_category,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY
    review_score,
    CASE
        WHEN review_score <= 2 THEN 'Poor'
        WHEN review_score = 3 THEN 'Neutral'
        WHEN review_score >= 4 THEN 'Good'
    END
ORDER BY review_score;


-- Insight 8:
-- Calculate the total number of orders for each year.
SELECT
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY EXTRACT(YEAR FROM order_purchase_timestamp)
ORDER BY year;


-- Insight 9:
-- Calculate the average delivery time for each year.
SELECT
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date
                    - order_purchase_timestamp
                )
            ) / 86400
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY EXTRACT(YEAR FROM order_purchase_timestamp)
ORDER BY year;


-- Insight 10:
-- Find products whose total revenue is greater than
-- the average revenue across all products.
SELECT
    product_id,
    total_revenue
FROM (
    SELECT
        product_id,
        SUM(price) AS total_revenue
    FROM order_items
    GROUP BY product_id
) product_revenue
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM (
        SELECT
            product_id,
            SUM(price) AS total_revenue
        FROM order_items
        GROUP BY product_id
    ) avg_product_revenue
)
ORDER BY total_revenue DESC;