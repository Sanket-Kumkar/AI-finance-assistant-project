import plotly.express as px
import streamlit as st
import pandas as pd
from ai.ai_categorization import categorize_transactions
from parsers.hdfc_parser import parse_hdfc
from processing.clean_transactions import clean_transactions
from analysis.financial_metrics import calculate_metrics
from analysis.health_score import calculate_health_score


st.set_page_config(page_title="AI Finance Analyzer", layout="wide")

st.title("💰 AI-Powered Finance Analyzer")

st.markdown("Upload your bank statement and get instant financial insights.")

bank = st.selectbox(
    "Select Bank",
    ["HDFC Bank"]
)

uploaded_file = st.file_uploader(
    "Upload Bank Statement (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file:
    
    st.write("File uploaded successfully:", uploaded_file.name)

    if bank == "HDFC Bank":
        transactions = parse_hdfc(uploaded_file)
    
    st.write("Number of transactions:", len(transactions))

    transactions = clean_transactions(transactions)

    transactions = categorize_transactions(transactions)

    metrics = calculate_metrics(transactions)

    health_score = calculate_health_score(metrics, transactions)

    st.subheader("💡 Financial Health Score")

    st.metric("Score", f"{health_score} / 100")

    if health_score >= 80:
        st.success("Excellent financial health! Keep it up.")
    elif health_score >= 60:
        st.warning("Good, but there is room for improvement.")
    else:
        st.error("Your financial health needs attention.")

    st.subheader("📊 Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Income", f"₹ {metrics['income']}")
    col2.metric("Expenses", f"₹ {metrics['expense']}")
    col3.metric("Savings", f"₹ {metrics['savings']}")
    col4.metric("Cash Withdrawn", f"₹ {metrics['cash']}")

    st.subheader("📊 Spending Breakdown")

    df = pd.DataFrame(transactions)

    # Only expenses
    expense_df = df[df["amount"] < 0].copy()

    expense_df["amount"] = expense_df["amount"].abs()

    category_summary = expense_df.groupby("category")["amount"].sum().reset_index()

    if not category_summary.empty:
        fig = px.pie(
            category_summary,
            names="category",
            values="amount",
            title="Spending by Category"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Monthly Spending Trend")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly = df[df["amount"] < 0].copy()
    monthly["amount"] = monthly["amount"].abs()

    monthly_summary = monthly.groupby("month")["amount"].sum().reset_index()

    if not monthly_summary.empty:
        fig2 = px.line(
            monthly_summary,
            x="month",
            y="amount",
            markers=True,
            title="Monthly Expenses"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📄 Sample Transactions")

    df = pd.DataFrame(transactions)

    st.dataframe(df.head(20), use_container_width=True)
