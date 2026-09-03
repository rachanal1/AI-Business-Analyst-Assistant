import pandas as pd
from sqlalchemy import text
from sqlalchemy_database import engine


try:
    # SQL query
    query = text("""
        SELECT
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp
        FROM orders
        LIMIT 10;
    """)

    # Read PostgreSQL result directly into a Pandas DataFrame
    df = pd.read_sql(query, engine)

    print("Pandas connection successful!")
    print("\nFirst 10 orders:")
    print(df)

    print("\nDataFrame shape:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

except Exception as e:
    print("Pandas test failed.")
    print("Error:", e)