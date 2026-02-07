from fastapi import FastAPI
from .db import Base, engine
from .routers import employees, payrolls
from . import models


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="University Payroll API (OOP style)")

app.include_router(employees.router)
app.include_router(payrolls.router)


@app.on_event("startup")
def startup_event():
    create_tables()
