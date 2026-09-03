import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Load variables from .env
load_dotenv()

# Read PostgreSQL settings
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Display settings except the password
print("USER:", DB_USER)
print("HOST:", DB_HOST)
print("PORT:", DB_PORT)
print("DATABASE:", DB_NAME)
print("PASSWORD SET:", bool(DB_PASSWORD))

# Create the database URL safely.
# URL.create() handles special characters such as @ in the password.
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

print("SQLAlchemy database engine created successfully.")