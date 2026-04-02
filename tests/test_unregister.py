"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.
"""


class TestUnregisterSuccess:
    """Test successful unregister scenarios."""

    def test_unregister_existing_participant(self, client, reset_activities):
        """Test successful removal of an existing participant."""
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email_to_remove in data["message"]
        assert activity_name in data["message"]

        # Verify participant was removed
        updated_response = client.get("/activities")
        updated_data = updated_response.json()
        assert email_to_remove not in updated_data[activity_name]["participants"]

    def test_unregister_last_participant(self, client, reset_activities):
        """Test unregistering when only one participant remains."""
        # Arrange
        activity_name = "Basketball Team"
        email = "test@mergington.edu"

        # Act
        signup_resp = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_resp.status_code == 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200


class TestUnregisterErrors:
    """Test error scenarios for unregister."""

    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregister from a non-existent activity returns 404."""
        # Arrange
        nonexistent_activity = "NonExistentActivity"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": "test@mergington.edu"}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_non_registered_student(self, client, reset_activities):
        """Test unregistering a student who is not registered returns error."""
        # Arrange
        activity_name = "Chess Club"
        non_registered_email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": non_registered_email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower()

    def test_unregister_from_empty_activity(self, client, reset_activities):
        """Test unregistering from an activity with no participants."""
        # Arrange
        activity_name = "Basketball Team"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": "test@mergington.edu"}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower()
