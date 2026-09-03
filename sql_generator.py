import os
from dotenv import load_dotenv
from google import genai

from langchain_core.prompts import PromptTemplate


load_dotenv()


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Create a reusable LangChain prompt template
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
1. Generate PostgreSQL SQL only.
2. Use only tables and columns provided in the schema.
3. Use the provided table relationships when JOINs are required.
4. Do not invent tables or columns.
5. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, GRANT, or REVOKE.
6. Generate only a SELECT or WITH query.
7. If the user's question refers to previous conversation,
   use the conversation context to understand what they mean.
8. Return only the SQL query.
9. Do not return Markdown code fences.
10. Do not provide an explanation.

USER QUESTION:
{question}
"""
)


def generate_sql(question, schema_context, conversation_history=None):

    # Convert conversation history into text
    if conversation_history:
        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in conversation_history
        )
    else:
        history_text = "No previous conversation."

    # Use LangChain to fill the prompt template
    prompt = sql_prompt.format(
        schema_context=schema_context,
        history_text=history_text,
        question=question
    )

    # Send the generated prompt to Gemini
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()