import re


def validate_sql(sql):
    """
    Validate AI-generated SQL before execution.
    Only SELECT or WITH queries are allowed.
    """

    cleaned_sql = sql.strip()

    # Remove Markdown code fences
    cleaned_sql = re.sub(
        r"^```(?:sql)?\s*|\s*```$",
        "",
        cleaned_sql,
        flags=re.IGNORECASE
    ).strip()

    # Only SELECT or WITH queries are allowed
    if not re.match(
        r"^(SELECT|WITH)\b",
        cleaned_sql,
        re.IGNORECASE
    ):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )

    # Block dangerous SQL operations
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE"
    ]

    for keyword in forbidden_keywords:

        if re.search(
            rf"\b{keyword}\b",
            cleaned_sql,
            re.IGNORECASE
        ):
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    # Prevent multiple SQL statements
    statements = [
        statement.strip()
        for statement in cleaned_sql.split(";")
        if statement.strip()
    ]

    if len(statements) > 1:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return cleaned_sql