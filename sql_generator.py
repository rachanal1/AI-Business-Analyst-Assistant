
import os
from dotenv import load_dotenv
from google import genai

from langchain_core.prompts import PromptTemplate


load_dotenv()


# --------------------------------------------------
# Create Gemini Client
# --------------------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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

Your task is to convert the user's business question
into a valid PostgreSQL SQL query.

DATABASE SCHEMA:
{schema_context}

RECENT CONVERSATION:
{history_text}

RULES:

GENERAL SQL RULES:
1. Generate PostgreSQL SQL only.
2. Use only tables and columns provided in the schema.
3. Use the provided table relationships when JOINs are required.
4. Do not invent tables or columns.
5. Do not use INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, GRANT, or REVOKE.
6. Generate only a SELECT or WITH query.
7. If the user's question refers to previous conversation,
   use the conversation context to understand what they mean.
8. Return only the SQL query.
9. Do not return Markdown code fences.
10. Do not provide an explanation.

REVENUE CALCULATION RULES:
11. For monthly revenue questions, use
    orders.order_purchase_timestamp to group orders by month.
12. Join orders to order_payments using order_id when
    payment_value is the requested revenue metric.
13. Calculate payment revenue using
    SUM(order_payments.payment_value).
14. Do not filter by order_status unless the user explicitly
    requests a particular order status.
15. Use clear aliases such as order_month and monthly_revenue.
16. Sort monthly results chronologically in ascending order.
17. Include all months returned by the query, including months
    with low revenue. Do not remove low-revenue months.
18. Do not invent missing months or fabricate zero-revenue rows.
19. Avoid duplicate counting by joining only through the
    appropriate keys and relationships in the schema.
20. If the user explicitly requests product sales revenue,
    use the appropriate product-price column instead of
    automatically treating payment_value as product revenue.

USER QUESTION:
{question}
"""
)


# --------------------------------------------------
# Generate SQL
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

    # Fill the prompt template
    prompt = sql_prompt.format(
        schema_context=schema_context,
        history_text=history_text,
        question=question
    )

    # Send prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    if not response.text:
        raise ValueError(
            "Gemini did not return a SQL query. Please try again."
        )

    return response.text.strip()
