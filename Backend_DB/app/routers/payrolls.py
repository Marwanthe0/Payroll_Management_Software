from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from ..services import payroll_service
from .. import models
from ..config import settings

router = APIRouter(prefix="/payrolls", tags=["payrolls"])


@router.post("/pay_month")
def pay_month(
    year: int = Query(..., ge=1900),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):
    return payroll_service.pay_all(db, year, month)


@router.get("/receipt/{employee_id}")
def get_salary_receipt(
    employee_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
):
    result = (
        db.query(models.Payroll, models.Employee)
        .join(models.Employee, models.Payroll.employee_id == models.Employee.id)
        .filter(
            models.Payroll.employee_id == employee_id,
            models.Payroll.year == year,
            models.Payroll.month == month,
            models.Employee.is_active == True,
        )
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Payroll not found")

    payroll, employee = result

    allowances = {}
    for a in settings.ALLOWANCES:
        display_name = settings.ALLOWANCE_NAMES.get(a, a.upper())
        allowances[display_name] = getattr(payroll, a, 0.0) or 0.0

    deductions = {}
    for d in settings.DEDUCTIONS:
        display_name = settings.DEDUCTION_NAMES.get(d, d.upper())
        deductions[display_name] = getattr(payroll, d, 0.0) or 0.0

    return {
        "employee_id": employee.id,
        "name": employee.name,
        "designation": employee.designation,
        "faculty": employee.faculty,
        "department": employee.department,
        "year": year,
        "month": month,
        "basic_salary": payroll.basic_salary,
        "allowances": allowances,
        "deductions": deductions,
    }


@router.get("/summary")
def get_summary(
    year: int,
    month: int,
    faculty: str | None = None,
    department: str | None = None,
    designation: str | None = None,
    db: Session = Depends(get_db),
):
    return payroll_service.payroll_summary(
        db, year, month, faculty, department, designation
    )
