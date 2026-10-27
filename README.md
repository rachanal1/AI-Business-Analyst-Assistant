# AI Business Analyst Assistant

An AI-powered business analytics application that allows users to ask business questions in natural language and receive SQL results, visualizations, and business insights.

## Live Demo

Try the application here: [AI Business Analyst Assistant](https://ai-business-analyst-assistant-lfa3iszcwvgenq8jxszu4k.streamlit.app/)

## Features

- Ask business questions using natural language
- Generate PostgreSQL SQL queries using Gemini
- Validate AI-generated SQL before execution
- Execute read-only queries against PostgreSQL
- Display query results in tables
- Generate business insights using Gemini
- Create visualizations using Plotly
- Support follow-up questions using conversation context
- Display business KPIs
- Maintain application logs

## Technologies Used

- Python
- PostgreSQL
- SQL
- Gemini API
- LangChain
- Pandas
- Plotly
- Streamlit
- SQLAlchemy
- Psycopg
- python-dotenv
- Git and GitHub

## Architecture

```text
User
  ↓
Streamlit Web Application
  ↓
Python Application
  ↓
Gemini API
  ↓
SQL Generation
  ↓
SQL Validation
  ↓
PostgreSQL Database
  ↓
Query Results
  ↓
Gemini API
  ↓
Business Explanation
  ↓
Dashboard with Results and Visualizations
```

## Database

The project uses an e-commerce dataset containing seven tables:

- `customers`
- `orders`
- `order_items`
- `products`
- `sellers`
- `order_payments`
- `order_reviews`

## Example Questions

- Show total orders
- Show the number of orders by status
- Show monthly revenue
- Which category has the highest revenue?
- Who are the top 10 customers by revenue?
- What is the average order value?
- What was the highest revenue month?

## SQL Security

The application validates AI-generated SQL before execution.

- Only `SELECT` and `WITH` queries are allowed.
- Data modification and schema modification operations are blocked.
- A read-only database user is used for analytics queries.
- Database credentials and API keys are stored in environment variables or hosting secrets.

Blocked operations include:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `TRUNCATE`
- `CREATE`
- `GRANT`
- `REVOKE`

## Project Structure

```text
AI-Business-Analyst-Assistant/
│
├── app.py
├── ai_business_analyst.py
├── conversation_manager.py
├── database.py
├── explanation_generator.py
├── logger.py
├── result_formatter.py
├── schema_context.py
├── sqlalchemy_database.py
├── sql_executor.py
├── sql_generator.py
├── sql_validator.py
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_data_quality_checks.sql
│   ├── 03_business_kpi_analysis.sql
│   ├── 04_insight_queries.sql
│   └── 05_readonly_permissions.sql
│
├── tests/
├── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rachanal1/AI-Business-Analyst-Assistant.git
cd AI-Business-Analyst-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows CMD:

```cmd
.venv\Scripts\activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```dotenv
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder values with your own database credentials and Gemini API key.

**Important:** Never commit your `.env` file, database passwords, or API keys to GitHub.

### 6. Set up PostgreSQL

Configure a PostgreSQL database and import the required e-commerce dataset.

The SQL scripts in the `sql/` folder contain table definitions, data quality checks, business KPI queries, insight queries, and read-only permission setup.

Ensure the database credentials in `.env` match your database configuration.

### 7. Run the application

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit, usually:

```text
http://localhost:8501
```

## Testing

The project includes individual test scripts inside the `tests/` folder.

For example, to test SQL validation:

```bash
python tests/test_validator.py
```

To test the SQLAlchemy database connection:

```bash
python tests/test_sqlalchemy.py
```

Other test scripts cover database connectivity, schema context, SQL generation, query execution, business explanations, conversation management, logging, Pandas, and Plotly.

## Deployment

The application is deployed using Streamlit Community Cloud, with PostgreSQL hosted on Neon.

- **Application hosting:** Streamlit Community Cloud
- **Database hosting:** Neon PostgreSQL
- **AI capabilities:** Gemini API
- **Source code:** GitHub

Live Demo: [AI Business Analyst Assistant](https://ai-business-analyst-assistant-lfa3iszcwvgenq8jxszu4k.streamlit.app/)


## Future Improvements

- Add authentication and access control
- Introduce more advanced business KPIs
- Support additional visualization types
- Add downloadable business reports
- Improve SQL validation and error handling
- Enhance conversational analytics
- Improve cloud reliability and monitoring
