import streamlit as st
import pandas as pd
import plotly.express as px
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
SAVINGS_FILE = BASE_DIR / "data" / "savings.csv"

# Load data
transactions = pd.read_csv(TRANSACTIONS_FILE)
savings_goals = pd.read_csv(SAVINGS_FILE)

#Calculate financial totals
income = transactions.loc[
  transactions["type"] == "Income", "amount"
].sum()

expenses = transactions.loc[
  transactions["type"] == "Expense", "amount"
].sum()

savings = transactions.loc[
  transactions["type"] == "Savings", "amount"
].sum()

debt_payments = transactions.loc[
  transactions["type"] == "Debt", "amount"
].sum()

# Calculate remaining money
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

# Spending analysis
st.subheader("Spending by Category")

expense_data = transactions[
  transactions["type"] == "Expense"
]

category_spending = (
  expense_data.groupby("category")["amount"]
  .sum()
  .reset_index()
  .sort_values("amount", ascending=False)
)

spending_chart = px.bar(
  category_spending,
  x="category",
  y="amount",
  labels={
    "category": "Category",
    "amount": "Amount ($)"
  },
  title="Expense Breakdown"
)

st.plotly_chart(
  spending_chart,
  use_container_width=True
)

# Savings goals
st.subheader("🎯 Savings Goals")

for _, goal in savings_goals.iterrows():

  goal_name = goal["goal"]
  target = goal["target_amount"]
  current = goal["current_amount"]

  if target > 0:
    progress = min(current / target, 1.0)
  else:
    progress = 0

remaining_goal = max(target - current, 0)

st.write(f"**{goal_name}**")

st.progress(progress)

col1, col2, col3 = st.columns(3)

col1.metric(
  "Saved",
  f"${current:,.2f}"
)

col2.metric(
  "Goal",
  f"${target:,.2f}"
)

col3.metric(
  "Remaining",
  f"%{remaining_goal:,.2f}"
)

st.caption(
  f"{progress:.0%} complete * Target date: {goal['target_date']}"
)

st.divider()
