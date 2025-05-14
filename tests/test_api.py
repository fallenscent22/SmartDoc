from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_document():
    response = client.post("/process", files={"file": ("test.txt", b"test content")})
    assert response.status_code == 200
    assert "file_key" in response.json()

def test_summarize():
    response = client.post("/summarize", json={"file_key": "test.txt"})
    assert response.status_code == 200
    assert "summary" in response.json()