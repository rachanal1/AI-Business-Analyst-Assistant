
import os
import time

from dotenv import load_dotenv
from google import genai
from langchain_core.prompts import PromptTemplate


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Create Gemini Client
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please configure it in your .env file or deployment secrets."
    )

client = genai.Client(
    api_key=api_key
)


# --------------------------------------------------
# SQL Generation Prompt
# --------------------------------------------------

sql_prompt = PromptTemplate(
    input_variables=[
        "schema_context",
        "history_text",
        "question"
    ],
    template="""
You are an AI Business Analyst.

Convert the user's business question into a valid
PostgreSQL SQL query.

DATABASE SCHEMA:
{schema_context}

RECENT CONVERSATION:
{history_text}

GENERAL SQL RULES:
1. Generate PostgreSQL SQL only.
2. Use only tables and columns provided in the schema.
3. Use the provided table relationships when JOINs are required.
4. Do not invent tables or columns.
5. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, GRANT, or REVOKE.
6. Generate only a SELECT or WITH query.
7. Use conversation history to understand follow-up questions.
8. Return only the SQL query.
9. Do not return Markdown code fences.
10. Do not include explanations.

MONTHLY REVENUE RULES:
11. For monthly revenue, group by
    orders.order_purchase_timestamp.
12. When calculating payment revenue, join orders and order_payments
    using order_id and calculate SUM(order_payments.payment_value).
13. Do not filter by order_status unless the user requests a
    particular order status.
14. Use clear aliases such as order_month and monthly_revenue.
15. Sort monthly results chronologically in ascending order.
16. Include all months returned by the query, including months
    with low revenue.
17. Do not invent missing months or fabricate zero-revenue rows.
18. Avoid joins that duplicate payment amounts.
19. If the user explicitly asks for product sales revenue,
    use the appropriate product-price metric instead.

USER QUESTION:
{question}
"""
)


# --------------------------------------------------
# Generate SQL with Retry Handling
# --------------------------------------------------

def generate_sql(
    question,
    schema_context,
    conversation_history=None
):

    # Convert conversation history into text
    if conversation_history:

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )

    else:

        history_text = "No previous conversation."

    # Create the prompt
    prompt = sql_prompt.format(
        schema_context=schema_context,
        history_text=history_text,
        question=question
    )

    # Retry temporary Gemini service errors
    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response. "
                    "Please try again."
                )

            return response.text.strip()

        except Exception as error:

            error_message = str(error).upper()

            temporary_error = any(
                marker in error_message
                for marker in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "INTERNAL",
                    "502",
                    "504",
                    "DEADLINE_EXCEEDED"
                ]
            )

            # Do not retry non-temporary errors
            if not temporary_error:
                raise

            # Stop after the final attempt
            if attempt == max_attempts - 1:
                raise

            # Wait 1 second, then 2 seconds before retrying
            time.sleep(2 ** attempt)

    raise RuntimeError(
        "Unable to generate SQL after multiple attempts."
    )
