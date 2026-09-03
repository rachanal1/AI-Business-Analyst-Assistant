from schema_context import get_schema_context
from sql_generator import generate_sql


question = "Which product category generated the highest revenue?"

schema = get_schema_context()

sql = generate_sql(question, schema)

print("=== GENERATED SQL ===")
print(sql)