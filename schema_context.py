from database import get_connection


def get_schema_context():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    schema_lines = []

    current_table = None

    for table_name, column_name, data_type in rows:

        if table_name != current_table:
            schema_lines.append(f"\nTABLE: {table_name}")
            current_table = table_name

        schema_lines.append(
            f"  - {column_name} ({data_type})"
        )

    relationships = """
    
TABLE RELATIONSHIPS:

customers.customer_id = orders.customer_id
orders.order_id = order_items.order_id
products.product_id = order_items.product_id
sellers.seller_id = order_items.seller_id
orders.order_id = order_payments.order_id
orders.order_id = order_reviews.order_id
"""

    schema_context = "\n".join(schema_lines) + relationships

    return schema_context