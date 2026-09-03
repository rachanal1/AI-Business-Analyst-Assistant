from sqlalchemy import text
from sqlalchemy_database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM orders;"))
        count = result.scalar()

        print("SQLAlchemy connection successful!")
        print("Total orders:", count)

except Exception as e:
    print("Database connection failed.")
    print("Error:", e)