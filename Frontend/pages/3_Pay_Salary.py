import streamlit as st
from services.api import pay_salary
import datetime

st.title("💸 Pay Monthly Salary")
st.markdown("Generate salary for **all employees** for a selected month")

st.divider()

# ---------- Inputs ----------
col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Year", min_value=2020, max_value=2100, value=datetime.datetime.now().year
    )

with col2:
    month = st.selectbox(
        "Month",
        [
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
        ],
        format_func=lambda x: x[1],
    )[0]

st.warning(
    """
    ⚠️ **Important Rules**
    - A month’s salary cannot be paid twice for the same employee.
    """
)

# ---------- Action ----------
if st.button("🚀 Pay Salary for All Employees"):
    with st.spinner("Processing payroll..."):
        success, result = pay_salary(year, month)

    if success:
        st.success("✅ Salary processed successfully!")

        st.subheader("📊 Result")
        st.json(result)

        if result.get("errors"):
            st.warning("Some employees were skipped due to rule violations.")
    else:
        st.error(f"❌ Payroll failed\n\n{result}")
