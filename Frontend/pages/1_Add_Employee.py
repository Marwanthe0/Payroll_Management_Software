import streamlit as st
from services.api import add_employee

st.title("➕ Add New Employee")
st.markdown("Fill in the employee details below")

st.divider()

# ---------- Form ----------
with st.form("add_employee_form"):
    col1, col2 = st.columns(2)

    with col1:
        emp_type = st.selectbox("Employee Type", ["teacher", "officer", "staff"])
        name = st.text_input("Full Name")

        age = st.number_input("Age", min_value=18, max_value=80, step=1)
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

    with col2:
        designation = st.text_input("Designation")
        faculty = st.text_input("Faculty")
        department = st.text_input("Department")
        basic_salary = st.number_input("Basic Salary", min_value=0.0, step=1000.0)

    submitted = st.form_submit_button("Add Employee")

# ---------- Form Submission ----------
if submitted:
    if not name or not emp_type:
        st.error("Name and Employee Type are required!")
    else:
        payload = {
            "emp_type": emp_type,
            "name": name,
            "age": age,
            "email": email,
            "phone": phone,
            "designation": designation,
            "faculty": faculty,
            "department": department,
            "basic_salary": basic_salary,
        }

        success, result = add_employee(payload)

        if success:
            st.success("✅ Employee added successfully!")
            st.json(result)
        else:
            st.error(f"❌ Failed to add employee\n\n{result}")
