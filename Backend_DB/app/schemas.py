from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    emp_type: str
    name: str
    age: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    designation: Optional[str] = None
    faculty: Optional[str] = None
    department: Optional[str] = None
    basic_salary: float = 0.0


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
