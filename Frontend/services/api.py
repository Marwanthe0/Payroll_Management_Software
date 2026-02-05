import requests

API_BASE = "http://127.0.0.1:8000"


def add_employee(data: dict):
    try:
        response = requests.post(f"{API_BASE}/employees/", json=data, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


def get_employees():
    try:
        response = requests.get(f"{API_BASE}/employees/", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


def pay_salary(year: int, month: int):
    try:
        response = requests.post(
            f"{API_BASE}/payrolls/pay_month",
            params={"year": year, "month": month},
            timeout=10,
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


def delete_employee(emp_id: int):
    try:
        response = requests.delete(f"{API_BASE}/employees/{emp_id}", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


def get_payroll_summary(year, month, faculty=None, department=None, designation=None):
    try:
        params = {"year": year, "month": month}

        if faculty:
            params["faculty"] = faculty
        if department:
            params["department"] = department
        if designation:
            params["designation"] = designation

        response = requests.get(
            f"{API_BASE}/payrolls/summary", params=params, timeout=5
        )

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text

    except Exception as e:
        return False, str(e)
