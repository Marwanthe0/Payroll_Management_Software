from sqlalchemy.orm import Session
from ..config import settings
from .. import models, crud


def can_pay_employee(
    db: Session, employee_id: int, year: int, month: int
) -> (bool, str):
    # Same month salary cannot be paid twice
    if crud.payroll_exists(db, employee_id, month, year):
        return False, "duplicate-month"

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
        # Calculate allowances
        allowance_vals = {}
        for name, rate in settings.ALLOWANCES.items():
            if isinstance(rate, float) and rate < 1:
                allowance_vals[name] = emp.basic_salary * rate
            else:
                allowance_vals[name] = rate

        # Calculate deductions
        deduction_vals = {}
        for name, rate in settings.DEDUCTIONS.items():
            if isinstance(rate, float) and rate < 1:
                deduction_vals[name] = emp.basic_salary * rate
            else:
                deduction_vals[name] = rate

        net = (
            emp.basic_salary
            + sum(allowance_vals.values())
            - sum(deduction_vals.values())
        )
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
        total += payroll.net_salary

    return {
        "year": year,
        "month": month,
        "total_paid": total,
    }
