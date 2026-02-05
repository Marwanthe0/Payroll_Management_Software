from sqlalchemy.orm import Session
from ..config import settings
from .. import models, crud
from ..domain.employee import Teacher, Officer, Staff, EmployeeBase


def prev_month(year: int, month: int):
    if month == 1:
        return (year - 1, 12)
    return (year, month - 1)


def any_future_exists(db: Session, employee_id: int, year: int, month: int) -> bool:
    return (
        db.query(models.Payroll)
        .filter(
            models.Payroll.employee_id == employee_id,
            (
                (models.Payroll.year > year)
                | ((models.Payroll.year == year) & (models.Payroll.month > month))
            ),
        )
        .first()
        is not None
    )


def can_pay_employee(
    db: Session, employee_id: int, year: int, month: int
) -> (bool, str):
    if crud.payroll_exists(db, employee_id, month, year):
        return False, "duplicate-month"
    if any_future_exists(db, employee_id, year, month):
        return False, "future-month-exists"
    latest = crud.latest_payroll_for_employee(db, employee_id)
    if latest:
        if (latest.year, latest.month) != prev_month(year, month):
            return False, "not-sequential"
    return True, "ok"


def pay_all(db: Session, year: int, month: int):
    employees = (
        db.query(models.Employee).filter(models.Employee.is_active == True).all()
    )
    created = []
    errors = {}
    for emp in employees:
        ok, reason = can_pay_employee(db, emp.id, year, month)
        if not ok:
            errors[emp.id] = reason
            continue
        domain_cls = {"teacher": Teacher, "officer": Officer, "staff": Staff}.get(
            emp.emp_type.lower(), EmployeeBase
        )
        domain_obj = domain_cls(
            id=emp.id,
            name=emp.name,
            basic_salary=emp.basic_salary,
            designation=emp.designation,
            faculty=emp.faculty,
            department=emp.department,
        )
        allowance_vals = {
            "hra": emp.basic_salary * 0.20,  # 20%
            "ta": emp.basic_salary * 0.10,  # 10%
            "medical": 2000.0,  # fixed
        }
        deduction_vals = {
            "tax": emp.basic_salary * 0.05,  # 5%
            "pf": emp.basic_salary * 0.03,  # 3%
        }

        net = domain_obj.net_salary(allowance_vals, deduction_vals)
        payroll = models.Payroll(
            employee_id=emp.id,
            month=month,
            year=year,
            basic_salary=emp.basic_salary,
            net_salary=net,
            **allowance_vals,
            **deduction_vals,
        )
        db.add(payroll)
        created.append(emp.id)
    db.commit()
    return {"created": created, "errors": errors}


def payroll_summary(
    db: Session,
    year: int,
    month: int,
    faculty: str | None = None,
    department: str | None = None,
    designation: str | None = None,
):
    query = (
        db.query(models.Payroll, models.Employee)
        .join(models.Employee, models.Payroll.employee_id == models.Employee.id)
        .filter(
            models.Payroll.year == year,
            models.Payroll.month == month,
            models.Employee.is_active == True,
        )
    )

    if faculty:
        query = query.filter(models.Employee.faculty == faculty)
    if department:
        query = query.filter(models.Employee.department == department)
    if designation:
        query = query.filter(models.Employee.designation == designation)

    total = 0.0

    for payroll, emp in query.all():
        allowances = sum((getattr(payroll, a, 0.0) or 0.0) for a in settings.ALLOWANCES)
        deductions = sum((getattr(payroll, d, 0.0) or 0.0) for d in settings.DEDUCTIONS)

        net = payroll.basic_salary + allowances - deductions
        total += net

    return {
        "year": year,
        "month": month,
        "total_paid": total,
    }
