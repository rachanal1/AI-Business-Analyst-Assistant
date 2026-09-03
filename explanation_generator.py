import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_explanation(question, sql, columns, rows):

    result_text = f"Columns: {columns}\nRows: {rows}"

    prompt = f"""
You are an AI Business Analyst Assistant.

The user asked:
{question}

The SQL query used was:
{sql}

The database returned:
{result_text}

Explain the result in simple business language.

Rules:
1. Directly answer the user's question.
2. Mention the important result or number.
3. Do not invent information that is not present in the database result.
4. Do not give unnecessary technical SQL details.
5. Keep the explanation concise, around 2 to 4 sentences.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()