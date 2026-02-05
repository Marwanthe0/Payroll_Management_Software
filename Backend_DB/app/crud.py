from sqlalchemy.orm import Session
from . import models, schemas
from typing import List


def create_employee(db: Session, employee_in: schemas.EmployeeCreate):
    db_emp = models.Employee(
        emp_type=employee_in.emp_type,
        name=employee_in.name,
        age=employee_in.age,
        phone=employee_in.phone,
        email=employee_in.email,
        designation=employee_in.designation,
        faculty=employee_in.faculty,
        department=employee_in.department,
        basic_salary=employee_in.basic_salary,
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp


def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()


def list_employees(db: Session, skip=0, limit=100):
    return (
        db.query(models.Employee)
        .filter(models.Employee.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def payroll_exists(db: Session, employee_id: int, month: int, year: int) -> bool:
    return (
        db.query(models.Payroll)
        .filter_by(employee_id=employee_id, month=month, year=year)
        .first()
        is not None
    )


def latest_payroll_for_employee(db: Session, employee_id: int):
    return (
        db.query(models.Payroll)
        .filter_by(employee_id=employee_id)
        .order_by(models.Payroll.year.desc(), models.Payroll.month.desc())
        .first()
    )


def delete_employee(db: Session, emp_id: int):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        return False, "Employee not found"

    emp.is_active = False  # 👈 SOFT DELETE
    db.commit()
    return True, "Employee deactivated successfully"
