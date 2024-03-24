# Run this test script with the following command:
# pytest test_with_testclient.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    msg_snippet = "Please use the API endpoints"
    assert response.status_code == 200
    assert response.json()['msg'][:len(msg_snippet)] == msg_snippet
