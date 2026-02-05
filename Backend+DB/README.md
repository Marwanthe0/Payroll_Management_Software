# University Payroll (FastAPI + OOP) - Minimal Example

This is a minimal, runnable FastAPI backend implementing an OOP-style payroll system.
It's intended for local development and learning (SQLite). It includes:
- Employee CRUD (Teacher / Officer / Staff types)
- Payroll "pay month" operation with rule checks (no duplicate, sequential enforcement)
- Payroll receipt lookup and month summary

## Quickstart

1. Create and activate a Python venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Open docs: http://127.0.0.1:8000/docs

## Notes
- This project uses SQLite for quick local tests.
- Allowances/deductions are defined in `app/config.py`. If you change those lists,
  you'll need to recreate the DB (dev) or use a migration tool (alembic) for production.
