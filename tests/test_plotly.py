import pandas as pd
import plotly.express as px
from sqlalchemy import text
from sqlalchemy_database import engine


try:
    query = text("""
        SELECT
            order_status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC;
    """)

    # Get data from PostgreSQL into Pandas
    df = pd.read_sql(query, engine)

    print("Data retrieved successfully!")
    print(df)

    # Create an interactive bar chart
    fig = px.bar(
        df,
        x="order_status",
        y="order_count",
        title="Orders by Status",
        labels={
            "order_status": "Order Status",
            "order_count": "Number of Orders"
        }
    )

    # Open the chart in your browser
    fig.write_html("orders_by_status.html")
    print("Chart created successfully: orders_by_status.html")

except Exception as e:
    print("Plotly test failed.")
    print("Error:", e)