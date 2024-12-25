import pytest
from fastapi.testclient import TestClient
from app.main import app

# Set up the TestClient to send HTTP requests to FastAPI app
client = TestClient(app)

# Test Case 1: Test the root endpoint (for example, a health check or status check)
def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

# Test Case 2: Test GET request for a specific mock analytics API (e.g., user data)
def test_get_user_data():
    response = client.get("/mock/user?user_id=1&name=Alice")
    assert response.status_code == 200
    # Test that the response is correctly formatted (JSON response)
    assert response.json() == {
        "user_id": "1",
        "name": "Alice"
    }

# Test Case 3: Test POST request for creating a new mock analytics API
def test_create_analytics_api():
    data = {
        "method": "GET",
        "response_template": '{"user_id": "{{ user_id }}", "activity": "{{ activity }}"}'
    }
    response = client.post("/mock/analytics/user_activity", json=data)
    assert response.status_code == 201
    assert response.json() == {
        "message": "API created successfully",
        "api_name": "mock/analytics/user_activity"
    }

# Test Case 4: Test invalid endpoint (404 error)
def test_invalid_api():
    response = client.get("/mock/non_existent_api")
    assert response.status_code == 404
    assert response.json() == {"detail": "API not found"}

# Test Case 5: Test dynamic response with query parameters
def test_dynamic_response():
    response = client.get("/mock/analytics/user_activity?user_id=2&activity=login")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "2",
        "activity": "login"
    }
