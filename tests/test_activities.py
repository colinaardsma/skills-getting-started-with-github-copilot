"""
Tests for GET /activities endpoint.
"""


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities."""
        # Arrange - No special setup needed, fixtures handle this

        # Act - Make the API request
        response = client.get("/activities")

        # Assert - Verify the response
        assert response.status_code == 200
        data = response.json()

        # Verify we get all 9 activities
        assert len(data) == 9

        # Verify key activities are present
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data

    def test_get_activities_contains_required_fields(self, client, reset_activities):
        """Test that each activity contains all required fields."""
        # Arrange - Define expected required fields
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act - Make the API request
        response = client.get("/activities")
        data = response.json()

        # Assert - Verify each activity has all required fields
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict), f"Activity {activity_name} is not a dict"
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity {activity_name} missing required fields"

    def test_get_activities_contains_participants(self, client, reset_activities):
        """Test that activities with participants show those participants."""
        # Arrange - No special setup needed

        # Act - Make the API request
        response = client.get("/activities")
        data = response.json()

        # Assert - Verify Chess Club has expected participants
        chess_club = data["Chess Club"]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert len(chess_club["participants"]) == 2

    def test_get_activities_empty_participant_list(self, client, reset_activities):
        """Test that activities with no participants show empty list."""
        # Arrange - No special setup needed

        # Act - Make the API request
        response = client.get("/activities")
        data = response.json()

        # Assert - Verify Basketball Team has empty participant list
        basketball_team = data["Basketball Team"]
        assert basketball_team["participants"] == []
        assert isinstance(basketball_team["participants"], list)

    def test_get_activities_response_structure(self, client, reset_activities):
        """Test the overall response structure."""
        # Arrange - No special setup needed

        # Act - Make the API request
        response = client.get("/activities")
        data = response.json()

        # Assert - Verify response structure and data types
        assert isinstance(data, dict)
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert isinstance(activity_data.get("description"), str)
            assert isinstance(activity_data.get("schedule"), str)
            assert isinstance(activity_data.get("max_participants"), int)
            assert isinstance(activity_data.get("participants"), list)
            assert activity_data.get("max_participants") > 0
