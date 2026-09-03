from sql_executor import execute_sql


sql = """
SELECT
    p.product_category_name,
    SUM(oi.price) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 1;
"""

columns, rows = execute_sql(sql)

print("COLUMNS:")
print(columns)

print("\nRESULT:")
for row in rows:
    print(row)