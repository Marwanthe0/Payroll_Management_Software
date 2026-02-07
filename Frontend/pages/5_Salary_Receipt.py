import streamlit as st
from services.api import get_salary_receipt
import datetime

st.title("🧾 Salary Receipt")
st.markdown("Employee-wise monthly salary slip")

st.divider()

# ---------- Inputs ----------
col1, col2, col3 = st.columns(3)

with col1:
    emp_id = st.number_input("Employee ID", min_value=1, step=1)

with col2:
    year = st.number_input(
        "Year", min_value=2020, max_value=2100, value=datetime.datetime.now().year
    )

with col3:
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

# ---------- Action ----------
if st.button("View Salary Receipt"):
    with st.spinner("Fetching salary receipt..."):
        success, result = get_salary_receipt(emp_id, year, month)

    if not success:
        st.error(f"Failed to fetch receipt\n\n{result}")

    else:
        st.success("Salary receipt generated")

        st.divider()
        st.subheader("👤 Employee Information")

        colA, colB = st.columns(2)

        with colA:
            st.write("**Name:**", result.get("name"))
            st.write("**Designation:**", result.get("designation"))
            st.write("**Faculty:**", result.get("faculty"))

        with colB:
            st.write("**Department:**", result.get("department"))
            st.write("**Month:**", f"{month}/{year}")

        st.divider()
        st.subheader("💰 Salary Breakdown")

        basic = result.get("basic_salary", 0)
        allowances = result.get("allowances", {})
        deductions = result.get("deductions", {})

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ➕ Allowances")
            st.write("Basic Salary:", basic)
            for k, v in allowances.items():
                st.write(f"{k}:", v)

        with col2:
            st.markdown("### ➖ Deductions")
            for k, v in deductions.items():
                st.write(f"{k}:", v)

        net_salary = basic + sum(allowances.values()) - sum(deductions.values())

        st.divider()
        st.metric("🟢 Net Salary", net_salary)
