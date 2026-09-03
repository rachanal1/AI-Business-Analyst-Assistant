from sql_validator import validate_sql


# Test 1: Valid SELECT query
valid_sql = """
SELECT COUNT(*)
FROM orders;
"""

try:
    result = validate_sql(valid_sql)
    print("VALID QUERY:")
    print(result)
except ValueError as e:
    print("VALIDATION FAILED:", e)


print("\n--------------------\n")


# Test 2: Dangerous query
dangerous_sql = """
DROP TABLE orders;
"""

try:
    result = validate_sql(dangerous_sql)
    print("DANGEROUS QUERY WAS ALLOWED:")
    print(result)
except ValueError as e:
    print("DANGEROUS QUERY BLOCKED:")
    print(e)

print("\n--------------------\n")


# Test 3: Multiple SQL statements
multiple_sql = """
SELECT COUNT(*) FROM orders;
DROP TABLE orders;
"""

try:
    result = validate_sql(multiple_sql)
    print("MULTIPLE STATEMENTS WERE ALLOWED:")
    print(result)
except ValueError as e:
    print("MULTIPLE STATEMENTS BLOCKED:")
    print(e)