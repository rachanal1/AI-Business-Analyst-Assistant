import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ai_business_analyst",
    user="postgres",
    password="Rachusql123@"
)

print("Database connection successful!")

connection.close()