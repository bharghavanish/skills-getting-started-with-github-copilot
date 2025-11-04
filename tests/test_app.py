import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    activities = client.get("/activities").json()
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    activities = client.get("/activities").json()
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_signup_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
