from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=schemas.EmployeeOut)
def create_employee(emp_in: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    emp = crud.create_employee(db, emp_in)
    return emp


@router.get("/", response_model=list[schemas.EmployeeOut])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_employees(db, skip, limit)


@router.get("/{emp_id}", response_model=schemas.EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, emp_id)
    if not emp:
        raise HTTPException(status_code=404, detail=" Employee data not found")
    return emp


@router.delete("/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    success, msg = crud.delete_employee(db, emp_id)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}
