from explanation_generator import generate_explanation


question = "Which product category generated the highest revenue?"

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

columns = [
    "product_category_name",
    "total_revenue"
]

rows = [
    ("beleza_saude", 1258681.34)
]

explanation = generate_explanation(
    question,
    sql,
    columns,
    rows
)

print("=== BUSINESS INSIGHT ===")
print(explanation)