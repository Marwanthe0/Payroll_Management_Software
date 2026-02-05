import streamlit as st
import pandas as pd
import matplotlib
import datetime
from services.api import get_employees, get_payroll_summary

# ---------- Page Config ----------
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2.5rem;
        }

        .hero {
            text-align: center;
            margin-bottom: 40px;
        }

        .hero h1 {
            font-size: 42px;
            color: #e5e7eb;
        }

        .hero p {
            font-size: 18px;
            color: #94a3b8;
        }

        .card {
            background: linear-gradient(135deg, #020617, #0f172a);
            border: 1px solid #1e293b;
            padding: 30px;
            border-radius: 18px;
            text-align: center;
            box🍃
            box-shadow: 0 15px 30px rgba(0,0,0,0.35);
        }

        .card-title {
            font-size: 18px;
            color: #93c5fd;
            margin-bottom: 12px;
        }

        .card-value {
            font-size: 34px;
            font-weight: bold;
            color: #f8fafc;
        }

        .hint-box {
            background: #020617;
            border: 1px dashed #334155;
            padding: 20px;
            border-radius: 14px;
            color: #cbd5f5;
            margin-top: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
st.sidebar.markdown("---")
st.sidebar.success("🟢 Backend Connected")

# ---------- Header / Hero ----------
st.markdown(
    """
    <div class="hero">
        <h1>🎓 University Payroll Management System</h1>
        <p>Streamlit Frontend • FastAPI Backend • OOP Based Architecture</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Fetch Data ----------
success, employees = get_employees()
total_employees = len(employees) if success else 0

# ---------- Dashboard Cards ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">👥 Total Employees</div>
            <div class="card-value">{total_employees}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">💸 Payroll Records</div>
            <div class="card-value">Auto</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <div class="card-title">📊 Monthly Expense</div>
            <div class="card-value">View</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ---------- Employee Distribution ----------
st.markdown("## 👥 Employee Distribution by Type")

if success and employees:
    df = pd.DataFrame(employees)

    if "emp_type" in df.columns:
        emp_type_count = df["emp_type"].value_counts()

        chart_df = emp_type_count.reset_index()
        chart_df.columns = ["Employee Type", "Count"]

        st.bar_chart(chart_df.set_index("Employee Type"), height=350)
    else:
        st.info("Employee type information not available.")
else:
    st.info("No employee data found.")
# ---------- Monthly Payroll Expense ----------
st.markdown("## 💰 Monthly Payroll Expense Overview")

today = datetime.date.today()

ok, summary = get_payroll_summary(year=today.year, month=today.month)

if ok and summary and summary.get("total_paid", 0) > 0:
    expense_df = pd.DataFrame(
        {
            "Month": [f"{today.month}/{today.year}"],
            "Total Expense": [summary["total_paid"]],
        }
    )

    st.bar_chart(expense_df.set_index("Month"))
else:
    st.info("No payroll data available for the selected month.")

# ---------- Info Section ----------
st.markdown(
    """
    <div class="hint-box">
        👉 <b>Use the sidebar</b> to manage employees, generate payroll,
        view monthly summaries, and download salary receipts.<br><br>
        This system demonstrates <b>Object-Oriented Design</b>,
        <b>Business Rule Enforcement</b>, and a clean <b>Client–Server Architecture</b>.
    </div>
    """,
    unsafe_allow_html=True,
)
