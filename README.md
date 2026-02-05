# 🧾 Payroll Management System

A full-stack **Payroll Management System** built using **FastAPI** for the backend and **Streamlit** for the frontend.  
The system follows **Object-Oriented Programming (OOP)** principles and simulates a real-world university payroll workflow.

---

## 🚀 Features

### 👥 Employee Management
- Multiple employee types: **Teacher, Officer, Staff**
- Add new employees with personal and salary details
- View employee list
- **Soft delete** employees (inactive employees are excluded from payroll)

### 💰 Payroll Management
- Pay salary for **all active employees** for a specific month
- Enforces real payroll rules:
  - No duplicate salary for the same month
  - Salary must be paid **sequentially**
  - Cannot pay past months if a future month exists

### ➕ Allowances & ➖ Deductions
- Allowances:
  - House Rent Allowance (HRA) – 20%
  - Travel Allowance (TA) – 10%
  - Medical Allowance – fixed amount
- Deductions:
  - Tax – 5%
  - Provident Fund (PF) – 3%

### 🧾 Salary Receipt
- Employee-wise monthly payslip
- Shows:
  - Employee information
  - Basic salary
  - Allowances
  - Deductions
  - Net salary (calculated dynamically)

### 📊 Payroll Summ
