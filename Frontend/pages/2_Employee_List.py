import streamlit as st
import pandas as pd
from services.api import get_employees, delete_employee

st.title("👥 Employee List")
st.divider()

# ---------- Load Employees ----------
with st.spinner("Loading employees..."):
    success, data = get_employees()

if not success:
    st.error(data)

elif len(data) == 0:
    st.warning("No employees found.")

else:
    df = pd.DataFrame(data)

    # Optional: cleaner column order
    preferred_cols = [
        "id",
        "name",
        "emp_type",
        "age",
        "designation",
        "faculty",
        "department",
        "basic_salary",
    ]
    df = df[[c for c in preferred_cols if c in df.columns]]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("🚫 Delete Employee")

    emp_id = st.number_input("Enter Employee ID", min_value=1, step=1)

    confirm = st.checkbox("I confirm Deletion of this employee")

    if st.button("Delete Employee"):
        if not confirm:
            st.warning("Please confirm Deletion first")
        else:
            ok, res = delete_employee(emp_id)
            if ok:
                st.success("Employee Deleted successfully")
                st.rerun()
            else:
                st.error(res)
