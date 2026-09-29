import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
  page_title="Personal Finance Tracker",
  page_icon="💰",
  layout="wide"
)

st.title("💰 Personal Finance Tracker")

st.write(
  "Track your spending, savings, debt, financial goals, "
  "and investments in one place."
)

# Locate the project's data folder
BASE_DIR = Path(__file__).resolve().parent.parent
TRANSACTIONS_FILE = BASE_DIR / "data" / "transactions.csv"

# Load transaction data
transactions = pd.read_csv(TRANSACtIONS_FILE)

#Calculate financial totals
income = transactions.loc[
  transactions["type"] == "Income", "amount"
].sum()

epxenses = transactions.loc[
  transactions["type"] = "Expense", "amount"
].sum()

savings = transactions.loc[
  transactions["type"] == "Savings", "amount"
].sum()

debt_payments = transactions.loc[
  transactions["type"] == "Debt", "amount"
].sum()

remaining = income - expenses - savings - debt_payments

# Dashboard
st.subheader("Financial Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Income", f"${income:,.2f}")
col2.metric("Expenses", f"${expenses:,.2f}")
col1.metric("Savings", f"${savings:,.2f}")
col1.metric("Debt Payments", f"${debt_payments:,.2f}")
col1.metric("Remaining", f"${remaining:,.2f}")

st.subheader("Transactions")

st.dataframe(
  transactions,
  use_container_width=True,
  hide_index=True
)
