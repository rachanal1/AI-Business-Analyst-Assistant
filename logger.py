import os
from datetime import datetime


LOG_DIR = "logs"


def save_log(question, sql, result, explanation):

    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    filename = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filepath = os.path.join(
        LOG_DIR,
        f"query_{filename}.txt"
    )

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("AI BUSINESS ANALYST LOG\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"Timestamp:\n{timestamp}\n\n")

        file.write("USER QUESTION:\n")
        file.write(question)
        file.write("\n\n")

        file.write("GENERATED SQL:\n")
        file.write(sql)
        file.write("\n\n")

        file.write("DATABASE RESULT:\n")
        file.write(str(result))
        file.write("\n\n")

        file.write("BUSINESS INSIGHT:\n")
        file.write(explanation)
        file.write("\n")

    return filepath