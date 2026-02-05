# Basic smoke tests - run with pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/docs")
    assert r.status_code in (200, 308)
