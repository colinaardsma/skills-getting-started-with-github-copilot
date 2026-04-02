"""
Pytest configuration and fixtures for FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a known state before each test."""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Play soccer and improve teamwork",
            "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Club": {
            "description": "Express creativity through painting and drawing",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Drama Club": {
            "description": "Act in plays and improve public speaking",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Debate Club": {
            "description": "Learn argumentation and debate topics",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and learn about science",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": []
        }
    }

    activities.clear()
    activities.update(original_activities)

    yield

    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Provide a sample valid email for testing."""
    return "student@mergington.edu"
