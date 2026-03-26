"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_success(client):
    """Test successfully signing up a new student for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_activity_not_found(client):
    """Test signing up for a non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_student(client):
    """Test signing up same student twice returns 400"""
    # First signup
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response1.status_code == 400
    data = response1.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_students_same_activity(client):
    """Test multiple different students can sign up for the same activity"""
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    response1 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/activities/Tennis Club/signup",
        params={"email": email2}
    )
    assert response2.status_code == 200


def test_signup_student_multiple_activities(client):
    """Test a student can sign up for multiple different activities"""
    email = "multiactivity@mergington.edu"
    
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/activities/Gym Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200


def test_signup_response_format(client):
    """Test signup response has correct format"""
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": "artist@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
