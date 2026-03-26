"""
Tests for the GET /activities endpoint
"""

import pytest


def test_get_activities_success(client):
    """Test successfully retrieving all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify response is a dictionary
    assert isinstance(activities, dict)
    
    # Verify key activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities
    

def test_get_activities_has_required_fields(client):
    """Test that each activity has all required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
            

def test_get_activities_participants_is_list(client):
    """Test that participants field is always a list"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"


def test_get_activities_max_participants_is_number(client):
    """Test that max_participants is a valid number"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"Activity '{activity_name}' max_participants should be an integer"
        assert activity_data["max_participants"] > 0, \
            f"Activity '{activity_name}' max_participants should be positive"
