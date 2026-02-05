import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="University Payroll Management", page_icon="💵", layout="wide"
)

# ---------- Custom CSS ----------
with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.title("🏛️ Payroll System")
st.sidebar.markdown("Admin Dashboard")

st.sidebar.success("Backend Connected")

st.markdown(
    """
    <h1 style='text-align:center;'>University Payroll Management System</h1>
    <p style='text-align:center; font-size:18px;'>
    Streamlit Frontend • FastAPI Backend • OOP Based Architecture
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------- Home Content ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👨‍🏫 Employees", "—")
with col2:
    st.metric("💸 Payroll Records", "—")
with col3:
    st.metric("📊 Monthly Expense", "—")

st.info(
    """
    👉 Use the **sidebar** to navigate through:
    - Add Employee  
    - Employee List  
    - Pay Salary  
    - Payroll Summary  
    - Salary Receipt
    """
)
