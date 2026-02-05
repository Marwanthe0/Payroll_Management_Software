import streamlit as st
from services.api import get_payroll_summary
import datetime

st.title("📊 Payroll Summary")
st.markdown("Monthly salary expenditure report")

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

st.divider()

st.subheader("🔎 Optional Filters")

col3, col4, col5 = st.columns(3)

with col3:
    faculty = st.text_input("Faculty (optional)")

with col4:
    department = st.text_input("Department (optional)")

with col5:
    designation = st.text_input("Designation (optional)")

# ---------- Action ----------
if st.button("Generate Summary"):
    with st.spinner("Calculating payroll summary..."):
        success, result = get_payroll_summary(
            year=year,
            month=month,
            faculty=faculty,
            department=department,
            designation=designation,
        )

    if success:
        st.success("Summary generated successfully")

        st.metric(label="💰 Total Salary Paid", value=f"{result.get('total_paid', 0)}")

        st.json(result)

    else:
        st.error(f"Failed to generate summary\n\n{result}")
