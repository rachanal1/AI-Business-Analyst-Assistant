\# AI Business Analyst Assistant



An AI-powered business analytics application that allows users to ask business questions in natural language and receive SQL results, visualizations, and business insights.



\## Features



\- Ask business questions using natural language

\- Generate PostgreSQL SQL queries using Gemini

\- Validate AI-generated SQL before execution

\- Execute read-only queries against PostgreSQL

\- Display query results

\- Generate business insights using Gemini

\- Create visualizations using Plotly

\- Support follow-up questions using conversation context

\- Display business KPIs



\## Technologies Used



\- Python

\- PostgreSQL

\- SQL

\- Gemini API

\- LangChain

\- Pandas

\- Plotly

\- Streamlit

\- SQLAlchemy

\- Psycopg

\- Git \& GitHub



\## Architecture



User

↓

Streamlit

↓

Python

↓

Gemini

↓

SQL Generation

↓

SQL Validation

↓

PostgreSQL

↓

Query Result

↓

Gemini

↓

Business Explanation

↓

Dashboard



\## Database



The project uses an e-commerce dataset containing:



\- customers

\- orders

\- order\_items

\- products

\- sellers

\- order\_payments

\- order\_reviews



\## Example Questions



\- Show total orders

\- Show orders by status

\- Show monthly revenue

\- Which category has the highest revenue?

\- Who are the top 10 customers by revenue?

\- What is the average order value?

\- What was the highest revenue month?



\## SQL Security



The application validates AI-generated SQL before execution.



Only SELECT and WITH queries are allowed.



The following operations are blocked:



\- INSERT

\- UPDATE

\- DELETE

\- DROP

\- ALTER

\- TRUNCATE

\- CREATE

\- GRANT

\- REVOKE



A read-only database user is used for analytics queries.



\## Project Structure



AI-Business-Analyst-Assistant/

│

├── app.py

├── ai\_business\_analyst.py

├── conversation\_manager.py

├── database.py

├── explanation\_generator.py

├── logger.py

├── result\_formatter.py

├── schema\_context.py

├── sqlalchemy\_database.py

├── sql\_executor.py

├── sql\_generator.py

├── sql\_validator.py

│

├── sql/

├── tests/

├── logs/

│

├── requirements.txt

├── .gitignore

└── README.md



\## How to Run



\### 1. Clone the repository



git clone <your-github-repository-url>



cd AI-Business-Analyst-Assistant



\### 2. Create virtual environment



python -m venv .venv



\### 3. Activate virtual environment



For Windows CMD:



.venv\\Scripts\\activate



\### 4. Install dependencies



pip install -r requirements.txt



\### 5. Configure environment variables



Create a `.env` file:



POSTGRES\_HOST=localhost  

POSTGRES\_PORT=5432  

POSTGRES\_DB=ai\_business\_analyst  

POSTGRES\_USER=analytics\_readonly  

POSTGRES\_PASSWORD=your\_database\_password  

GEMINI\_API\_KEY=your\_gemini\_api\_key



Do not upload the `.env` file to GitHub.



\### 6. Set up PostgreSQL



Create the `ai\_business\_analyst` database and run the SQL scripts inside the `sql` folder.



\### 7. Run the application



streamlit run app.py



The application will open at:



http://localhost:8501



\## Testing



Example:



python tests\\test\_validator.py



Other component tests are available inside the `tests` folder.



\## Future Improvements



\- Cloud deployment

\- Authentication

\- More advanced KPIs

\- More visualization options

\- Downloadable reports

\- Improved conversational analytics

