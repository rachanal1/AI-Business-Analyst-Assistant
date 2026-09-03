from schema_context import get_schema_context
from sql_generator import generate_sql
from sql_executor import execute_sql
from explanation_generator import generate_explanation
from result_formatter import format_results
from conversation_manager import ConversationManager
from logger import save_log


def answer_question(question, schema, conversation):

    print("\nGenerating SQL with AI...")

    sql = generate_sql(
        question,
        schema,
        conversation.get_history()
    )

    print("\n=== GENERATED SQL ===")
    print(sql)

    print("\nExecuting SQL...")

    columns, rows = execute_sql(sql)

    if not rows:

        print("\n=== RESULT ===")
        print("No data found for this question.")

        conversation.add_message(
            "user",
            question
        )

        conversation.add_message(
            "assistant",
            "No data was found for this question."
        )

        return {
            "question": question,
            "sql": sql,
            "columns": columns,
            "rows": [],
            "explanation": "No data was found for this question."
        }

    print("\n=== DATABASE RESULT ===")
    print(format_results(columns, rows))

    print("\nGenerating business explanation...")

    explanation = generate_explanation(
        question,
        sql,
        columns,
        rows
    )

    print("\n=== BUSINESS INSIGHT ===")
    print(explanation)

    # Save query log
    log_file = save_log(
        question,
        sql,
        rows,
        explanation
    )

    print("\nLog saved:")
    print(log_file)

    # Save conversation context
    conversation.add_message(
        "user",
        question
    )

    conversation.add_message(
        "assistant",
        explanation
    )

    # Return results so Streamlit can display them
    return {
        "question": question,
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "explanation": explanation
    }


def main():

    print("======================================")
    print("     AI BUSINESS ANALYST ASSISTANT")
    print("======================================")

    print("\nType 'exit' to close the application.")

    print("\nLoading database schema...")
    schema = get_schema_context()

    conversation = ConversationManager(
        max_history=5
    )

    while True:

        question = input(
            "\nAsk a business question: "
        ).strip()

        if question.lower() == "exit":

            print("\nGoodbye!")
            break

        if not question:

            print(
                "Please enter a business question."
            )
            continue

        try:

            answer_question(
                question,
                schema,
                conversation
            )

        except ValueError as error:

            print("\nSQL VALIDATION ERROR:")
            print(error)

        except Exception as error:

            print("\nAPPLICATION ERROR:")
            print(error)


if __name__ == "__main__":
    main()