-- ============================================================
-- 02_data_quality_checks.sql
-- AI Business Analyst Assistant
-- Purpose:
-- Validate NULL values, uniqueness, duplicate records,
-- and basic completeness of the database tables.
-- ============================================================


-- Check whether any customer IDs are NULL.
SELECT COUNT(*) AS null_customer_ids
FROM customers
WHERE customer_id IS NULL;


-- Check total order rows and unique order IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids
FROM orders;


-- Check whether any order IDs are NULL.
SELECT COUNT(*) AS null_order_ids
FROM orders
WHERE order_id IS NULL;


-- Check total product rows and unique product IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_product_ids
FROM products;


-- Check whether any product IDs are NULL.
SELECT COUNT(*) AS null_product_ids
FROM products
WHERE product_id IS NULL;


-- Check total seller rows and unique seller IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT seller_id) AS unique_seller_ids
FROM sellers;


-- Check whether any seller IDs are NULL.
SELECT COUNT(*) AS null_seller_ids
FROM sellers
WHERE seller_id IS NULL;


-- Check total order-item rows and unique
-- order-item combinations.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (order_id, order_item_id)) AS unique_item_records
FROM order_items;


-- Check total payment rows and unique
-- order/payment-sequence combinations.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (order_id, payment_sequential)) AS unique_payment_records
FROM order_payments;


-- Check total review rows and unique generated review IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT review_record_id) AS unique_review_records
FROM order_reviews;


-- Check how many orders have each important
-- order lifecycle timestamp populated.
SELECT
    COUNT(*) AS total_orders,
    COUNT(order_approved_at) AS approved_orders,
    COUNT(order_delivered_carrier_date) AS carrier_delivered,
    COUNT(order_delivered_customer_date) AS customer_delivered,
    COUNT(order_estimated_delivery_date) AS estimated_delivery
FROM orders;


-- Analyze the distribution of order statuses.
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- Compare total customer records with unique customer IDs.
SELECT
    COUNT(*),
    COUNT(DISTINCT customer_id)
FROM customers;


-- Compare total order records with unique order IDs.
SELECT
    COUNT(*),
    COUNT(DISTINCT order_id)
FROM orders;


-- Compare total product records with unique product IDs.
SELECT
    COUNT(*),
    COUNT(DISTINCT product_id)
FROM products;


-- Compare total seller records with unique seller IDs.
SELECT
    COUNT(*),
    COUNT(DISTINCT seller_id)
FROM sellers;