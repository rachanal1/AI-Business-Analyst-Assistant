from database import get_connection
from sql_validator import validate_sql


def execute_sql(sql):
    # Validate the SQL first
    safe_sql = validate_sql(sql)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(safe_sql)

        # Get column names
        columns = [
            description.name
            for description in cursor.description
        ]

        # Get rows
        rows = cursor.fetchall()

        return columns, rows

    finally:
        cursor.close()
        connection.close()