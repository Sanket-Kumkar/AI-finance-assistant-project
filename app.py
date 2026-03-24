import plotly.express as px
import streamlit as st
import pandas as pd
from ai.ai_categorization import categorize_transactions
from parsers.hdfc_parser import parse_hdfc
from parsers.csv_parser import parse_csv
from processing.clean_transactions import clean_transactions
from analysis.financial_metrics import calculate_metrics
from analysis.health_score import calculate_health_score
from ai.ai_advisor import generate_advice
from analysis.scenario_simulator import simulate_savings,simulate_multi_savings


st.set_page_config(page_title="AI Finance Analyzer", layout="wide")

st.title("💰 AI-Powered Finance Analyzer")

st.markdown("Upload your bank statement and get instant financial insights.")

bank = st.selectbox(
    "Select Bank",
    ["HDFC Bank","SBI (Coming Soon)", "Axis (Coming Soon)"]
)
if bank != "HDFC Bank":
    st.warning("Support for this bank is under development.")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload Bank Statement (CSV / Excel/ pdf)",
    type=["csv", "xlsx","pdf"]
)

if uploaded_file is not None:

    file_type = uploaded_file.name.split(".")[-1].lower()

if uploaded_file:
    
    st.write("File uploaded successfully:", uploaded_file.name)

    if file_type == "csv":
        transactions = parse_csv(uploaded_file)

    elif file_type == "pdf":
        transactions = parse_hdfc(uploaded_file)

    else:
        st.error("Unsupported file format")
        st.stop()
    
    st.success(f"{file_type.upper()} file processed successfully")
    
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
    category_dict = dict(zip(category_summary["category"], category_summary["amount"]))

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


    advice = generate_advice(metrics, category_dict, health_score)
    
    st.subheader("🤖 AI Financial Advice")

    st.info(advice)

    st.subheader("🔮 Scenario Simulator")


    categories = df[df["amount"] < 0]["category"].unique()

    selected_categories = st.multiselect(
        "Select categories to reduce spending",
        categories
    )

    reduction_inputs = {}

    for cat in selected_categories:
        reduction_inputs[cat] = st.number_input(
            f"Reduction for {cat} (₹)",
            min_value=0,
            step=100,
            value=500
        )

    if st.button("Simulate"):

        new_metrics = simulate_multi_savings(
            transactions,
            metrics,
            reduction_inputs
        )

        st.subheader("📊 Simulation Result")

        col1, col2, col3 = st.columns(3)

        col1.metric("New Savings", f"₹ {int(new_metrics['savings']):,}")
        col2.metric(
            "Savings Increase",
            f"₹ {int(new_metrics['savings'] - metrics['savings']):,}"
        )

        new_health_score = calculate_health_score(new_metrics, transactions)

        col3.metric("New Score", f"{new_health_score}/100")