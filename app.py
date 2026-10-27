
import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import text
from sqlalchemy_database import engine

from schema_context import get_schema_context
from ai_business_analyst import answer_question
from conversation_manager import ConversationManager


# --------------------------------------------------
# Dashboard KPI Function
# --------------------------------------------------

def get_dashboard_kpis():

    with engine.connect() as connection:

        total_orders = connection.execute(
            text("SELECT COUNT(*) FROM orders;")
        ).scalar()

        total_customers = connection.execute(
            text("SELECT COUNT(*) FROM customers;")
        ).scalar()

        total_revenue = connection.execute(
            text("""
                SELECT COALESCE(SUM(payment_value), 0)
                FROM order_payments;
            """)
        ).scalar()

        average_order_value = connection.execute(
            text("""
                SELECT COALESCE(AVG(order_total), 0)
                FROM (
                    SELECT
                        order_id,
                        SUM(payment_value) AS order_total
                    FROM order_payments
                    GROUP BY order_id
                ) AS order_totals;
            """)
        ).scalar()

    return (
        total_orders,
        total_customers,
        total_revenue,
        average_order_value
    )


# --------------------------------------------------
# Visualization Function
# --------------------------------------------------

def create_visualization(df):

    if df.empty or len(df.columns) < 2 or len(df) == 1:
        return None

    df = df.copy()
    columns = df.columns.tolist()

    # --------------------------------------------------
    # Find Date Column First
    # --------------------------------------------------

    date_column = None

    for column in columns:

        is_likely_date = (
            column.lower() in [
                "date",
                "month",
                "year",
                "timestamp",
                "order_date",
                "order_month"
            ]
            or "date" in column.lower()
            or "timestamp" in column.lower()
            or column.lower().endswith("_month")
        )

        if (
            pd.api.types.is_datetime64_any_dtype(df[column])
            or is_likely_date
        ):

            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            if converted_dates.notna().all():
                date_column = column
                df[column] = converted_dates
                break

    # --------------------------------------------------
    # Find Numeric Columns
    # --------------------------------------------------

    numeric_columns = []

    for column in columns:

        if column == date_column:
            continue

        converted = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if converted.notna().any():
            df[column] = converted
            numeric_columns.append(column)

    if not numeric_columns:
        return None

    # --------------------------------------------------
    # Time Series -> Line Chart
    # --------------------------------------------------

    if date_column is not None:

        value_column = next(
            (
                column
                for column in numeric_columns
                if column != date_column
            ),
            None
        )

        if value_column is not None:

            df = df.dropna(
                subset=[date_column, value_column]
            )

            df = df.sort_values(
                by=date_column
            )

            if not df.empty:

                fig = px.line(
                    df,
                    x=date_column,
                    y=value_column,
                    title="Monthly Payment Revenue Trend",
                    markers=True,
                    labels={
                        date_column: "Month",
                        value_column: "Revenue"
                    }
                )

                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Revenue",
                    title_x=0.02
                )

                fig.update_traces(
                    connectgaps=False
                )

                return fig

    # --------------------------------------------------
    # Find Category Column
    # --------------------------------------------------

    category_column = next(
        (
            column
            for column in columns
            if column not in numeric_columns
            and column != date_column
        ),
        None
    )

    # --------------------------------------------------
    # Category + Numeric
    # --------------------------------------------------

    if category_column is not None:

        value_column = numeric_columns[0]

        if len(df) <= 6:

            return px.pie(
                df,
                names=category_column,
                values=value_column,
                title=f"{value_column} by {category_column}"
            )

        return px.bar(
            df,
            x=category_column,
            y=value_column,
            title=f"{value_column} by {category_column}"
        )

    # --------------------------------------------------
    # Multiple Numeric Columns -> Bar Chart
    # --------------------------------------------------

    if len(numeric_columns) >= 2:

        return px.bar(
            df,
            x=columns[0],
            y=numeric_columns[:3],
            title="Business Metrics"
        )

    return None


# --------------------------------------------------
# Business Question Validation
# --------------------------------------------------

def is_valid_business_question(question):

    vague_questions = [
        "hello",
        "hi",
        "hey",
        "tell me something",
        "give me information",
        "random text",
        "what can you do?",
        "what can you do",
        "who are you?",
        "who are you",
        "help",
        "help me"
    ]

    cleaned_question = question.strip().lower()

    return cleaned_question not in vague_questions


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("📊 AI Business Analyst")

    st.write(
        "Ask business questions about the e-commerce "
        "data using natural language."
    )

    st.divider()

    st.subheader("💡 Example Questions")

    example_questions = [
        "Show the number of orders by status",
        "Show monthly revenue",
        "Which category has the highest revenue?",
        "Who are the top 10 customers by revenue?",
        "What is the average order value?"
    ]

    for example in example_questions:

        if st.button(
            example,
            use_container_width=True
        ):
            st.session_state.selected_question = example

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.conversation = ConversationManager(
            max_history=5
        )

        st.session_state.selected_question = ""

        st.rerun()

    st.divider()

    st.caption("AI Business Analyst Assistant")

    st.caption(
        "PostgreSQL • Gemini • LangChain • Pandas • Plotly"
    )


# --------------------------------------------------
# Main Page
# --------------------------------------------------

st.title("AI Business Analyst Assistant")

st.write(
    "Ask a business question and get AI-generated SQL, "
    "database results, visualizations, and business insights."
)


# --------------------------------------------------
# Dashboard KPIs
# --------------------------------------------------

try:

    (
        total_orders,
        total_customers,
        total_revenue,
        average_order_value
    ) = get_dashboard_kpis()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            f"{total_orders:,}"
        )

    with col2:
        st.metric(
            "Total Customers",
            f"{total_customers:,}"
        )

    with col3:
        st.metric(
            "Revenue",
            f"{float(total_revenue):,.2f}"
        )

    with col4:
        st.metric(
            "Average Order Value",
            f"{float(average_order_value):,.2f}"
        )

except Exception as error:

    st.warning(
        f"Could not load dashboard KPIs: {error}"
    )


st.divider()


# --------------------------------------------------
# Load Database Schema
# --------------------------------------------------

@st.cache_resource
def load_schema():
    return get_schema_context()


schema = load_schema()


# --------------------------------------------------
# Conversation Management
# --------------------------------------------------

if "conversation" not in st.session_state:

    st.session_state.conversation = ConversationManager(
        max_history=5
    )

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

conversation = st.session_state.conversation


# --------------------------------------------------
# Question Input
# --------------------------------------------------

question = st.text_input(
    "Ask your business question:",
    value=st.session_state.selected_question,
    placeholder="Example: Show monthly revenue"
)


# --------------------------------------------------
# Ask Business Analyst
# --------------------------------------------------

if st.button(
    "🔍 Ask Business Analyst",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

    elif not is_valid_business_question(question):

        st.warning(
            "Please ask a specific business question "
            "about the e-commerce data."
        )

    else:

        with st.spinner("Analyzing your question..."):

            try:

                result = answer_question(
                    question,
                    schema,
                    conversation
                )

                # Business Question
                st.subheader("📝 Business Question")
                st.info(result["question"])

                # Generated SQL
                with st.expander(
                    "🔹 View Generated SQL",
                    expanded=False
                ):

                    st.code(
                        result["sql"],
                        language="sql"
                    )

                # Query Result
                df = pd.DataFrame(
                    result["rows"],
                    columns=result["columns"]
                )

                with st.expander(
                    "📋 View Query Result",
                    expanded=True
                ):

                    if not df.empty:

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "No data was found for this question."
                        )

                # Visualization
                if not df.empty:

                    fig = create_visualization(df)

                    if fig is not None:

                        with st.expander(
                            "📊 View Visualization",
                            expanded=True
                        ):

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                    else:

                        st.info(
                            "A suitable visualization "
                            "is not needed for this result."
                        )

                # Business Insight
                with st.expander(
                    "💡 Business Insight",
                    expanded=True
                ):

                    st.write(result["explanation"])

            except ValueError as error:

                st.error(
                    f"SQL Validation Error: {error}"
                )

            except Exception as error:

                st.error(
                    f"Application Error: {error}"
                )
