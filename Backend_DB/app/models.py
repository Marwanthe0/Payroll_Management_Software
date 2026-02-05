from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    emp_type = Column(String, index=True)  # teacher / officer / staff
    name = Column(String, nullable=False)
    age = Column(Integer)
    phone = Column(String)
    email = Column(String, unique=True, nullable=True)
    designation = Column(String)
    faculty = Column(String, nullable=True)
    department = Column(String, nullable=True)
    basic_salary = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)

    payrolls = relationship("Payroll", back_populates="employee")


class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True,
    )

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    basic_salary = Column(Float, default=0.0)
    net_salary = Column(Float, default=0.0)

    # -------- Allowances --------
    hra = Column(Float, default=0.0)
    ta = Column(Float, default=0.0)
    medical = Column(Float, default=0.0)

    # -------- Deductions --------
    tax = Column(Float, default=0.0)
    pf = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    employee = relationship("Employee", back_populates="payrolls")

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "month",
            "year",
            name="uq_employee_month_year",
        ),
    )
