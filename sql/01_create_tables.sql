-- ============================================================
-- 01_create_tables.sql
-- AI Business Analyst Assistant
-- Purpose:
-- Create the PostgreSQL tables used by the project
-- and perform basic verification after table creation.
-- ============================================================


-- Check the name of the PostgreSQL database currently connected to.
SELECT current_database();


-- ============================================================
-- CUSTOMERS TABLE
-- Purpose:
-- Stores customer identification and location information.
-- ============================================================

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INTEGER,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);


-- Preview the first 10 records from the customers table.
SELECT *
FROM customers
LIMIT 10;


-- Count the total number of records in the customers table.
SELECT COUNT(*)
FROM customers;


-- ============================================================
-- ORDERS TABLE
-- Purpose:
-- Stores order information, order status,
-- and order lifecycle timestamps.
-- ============================================================

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);


-- Preview the first 10 records from the orders table.
SELECT *
FROM orders
LIMIT 10;


-- Count the total number of order records.
SELECT COUNT(*)
FROM orders;


-- Check the total number of order rows
-- and the number of unique order IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders
FROM orders;


-- ============================================================
-- PRODUCTS TABLE
-- Purpose:
-- Stores product details including category,
-- dimensions, weight, description length, and photos.
-- ============================================================

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);


-- Count the total number of product records.
SELECT COUNT(*)
FROM products;


-- Check the total number of product rows
-- and unique product IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_products
FROM products;


-- ============================================================
-- SELLERS TABLE
-- Purpose:
-- Stores seller identification and location information.
-- ============================================================

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
);


-- Count the total number of seller records.
SELECT COUNT(*)
FROM sellers;


-- Check the total number of seller rows
-- and unique seller IDs.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT seller_id) AS unique_sellers
FROM sellers;


-- ============================================================
-- ORDER_ITEMS TABLE
-- Purpose:
-- Stores individual products belonging to orders,
-- including seller, price, and freight information.
-- ============================================================

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INTEGER,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    PRIMARY KEY (order_id, order_item_id)
);


-- Count the total number of order-item records.
SELECT COUNT(*)
FROM order_items;


-- Check total order-item rows,
-- unique orders, and unique products.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT product_id) AS unique_products
FROM order_items;


-- ============================================================
-- ORDER_PAYMENTS TABLE
-- Purpose:
-- Stores payment information for orders,
-- including payment type, installments, and payment value.
-- ============================================================

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INTEGER,
    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(10,2),
    PRIMARY KEY (order_id, payment_sequential)
);


-- Count the total number of payment records.
SELECT COUNT(*)
FROM order_payments;


-- Check total payment rows
-- and unique orders represented in the payment table.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders
FROM order_payments;


-- ============================================================
-- ORDER_REVIEWS TABLE
-- Purpose:
-- Stores customer review information,
-- including scores, comments, and review timestamps.
-- ============================================================

CREATE TABLE order_reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);


-- Count the total number of review records.
SELECT COUNT(*)
FROM order_reviews;


-- Count the total number of reviews.
SELECT COUNT(*) AS total_reviews
FROM order_reviews;


-- Check total review rows,
-- unique review IDs, and unique orders.
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT review_id) AS unique_review_ids,
    COUNT(DISTINCT order_id) AS unique_orders
FROM order_reviews;


-- Add a generated identity column to uniquely identify
-- every review record.
ALTER TABLE order_reviews
ADD COLUMN review_record_id BIGINT GENERATED ALWAYS AS IDENTITY;


-- Make the generated review_record_id the primary key.
ALTER TABLE order_reviews
ADD CONSTRAINT order_reviews_pk
PRIMARY KEY (review_record_id);