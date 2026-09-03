from decimal import Decimal


def format_value(value):
    if isinstance(value, Decimal):
        return f"{value:,.2f}"

    if isinstance(value, float):
        return f"{value:,.2f}"

    if isinstance(value, int):
        return f"{value:,}"

    return str(value)


def format_results(columns, rows):

    if not rows:
        return "No data found."

    lines = []

    # Header
    lines.append(" | ".join(columns))

    # Separator
    lines.append("-" * 80)

    # Data
    for row in rows:
        formatted_row = [
            format_value(value)
            for value in row
        ]

        lines.append(" | ".join(formatted_row))

    return "\n".join(lines)