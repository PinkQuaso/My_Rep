"""
Tests for the POST /activities/{activity_name}/unregister endpoint
"""

import pytest


def test_unregister_success(client):
    """Test successfully unregistering a student from an activity"""
    # First, sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "temp@mergington.edu"}
    )
    
    # Then unregister
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "temp@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert "temp@mergington.edu" in data["message"]


def test_unregister_existing_participant(client):
    """Test unregistering an existing participant from an activity"""
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]


def test_unregister_activity_not_found(client):
    """Test unregistering from a non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_registered(client):
    """Test unregistering a student not in the activity returns 400"""
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": "notregistered@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_then_signup_again(client):
    """Test a student can sign up again after unregistering"""
    email = "togglestudent@mergington.edu"
    
    # Sign up
    response1 = client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Unregister
    response2 = client.post(
        "/activities/Drama Club/unregister",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Sign up again
    response3 = client.post(
        "/activities/Drama Club/signup",
        params={"email": email}
    )
    assert response3.status_code == 200


def test_unregister_response_format(client):
    """Test unregister response has correct format"""
    # First sign up to ensure we can unregister
    client.post(
        "/activities/Science Club/signup",
        params={"email": "scientist@mergington.edu"}
    )
    
    response = client.post(
        "/activities/Science Club/unregister",
        params={"email": "scientist@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
