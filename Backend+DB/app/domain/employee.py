from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class EmployeeBase:
    id: Optional[int]
    name: str
    basic_salary: float
    designation: Optional[str] = None
    faculty: Optional[str] = None
    department: Optional[str] = None

    def compute_allowances(self, allowance_values: Dict[str, float]) -> float:
        return sum(allowance_values.values())

    def compute_deductions(self, deduction_values: Dict[str, float]) -> float:
        return sum(deduction_values.values())

    def net_salary(self, allowance_values: Dict[str, float], deduction_values: Dict[str, float]) -> float:
        return self.basic_salary + self.compute_allowances(allowance_values) - self.compute_deductions(deduction_values)

class Teacher(EmployeeBase):
    pass

class Officer(EmployeeBase):
    pass

class Staff(EmployeeBase):
    pass
