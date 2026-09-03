from logger import save_log


filepath = save_log(
    question="Which product category generated the highest revenue?",

    sql="""
SELECT
    p.product_category_name,
    SUM(oi.price) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 1;
""",

    result=[
        ("beleza_saude", 1258681.34)
    ],

    explanation=(
        "The beleza_saude category generated "
        "the highest revenue at approximately "
        "1.26 million."
    )
)

print("Log saved successfully:")
print(filepath)