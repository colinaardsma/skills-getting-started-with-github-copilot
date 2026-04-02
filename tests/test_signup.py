"""
Tests for POST /activities/{activity_name}/signup endpoint.
"""


class TestSignupSuccess:
    """Test successful signup scenarios."""

    def test_signup_valid_activity_valid_email(self, client, reset_activities, sample_email):
        """Test successful signup to an available activity."""
        # Arrange
        activity_name = "Basketball Team"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities, sample_email):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        activity_name = "Basketball Team"

        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_participants = len(initial_data[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": sample_email})

        # Assert
        updated_response = client.get("/activities")
        updated_data = updated_response.json()
        updated_participants = updated_data[activity_name]["participants"]

        assert len(updated_participants) == initial_participants + 1
        assert sample_email in updated_participants

    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """Test that multiple students can sign up for the same activity."""
        # Arrange
        activity_name = "Soccer Club"
        emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        response = client.get("/activities")
        data = response.json()
        participants = data[activity_name]["participants"]
        assert len(participants) == 3
        for email in emails:
            assert email in participants


class TestSignupErrors:
    """Test error scenarios for signup."""

    def test_signup_nonexistent_activity(self, client, reset_activities, sample_email):
        """Test signup to a non-existent activity returns 404."""
        # Act
        response = client.post(
            "/activities/NonExistentActivity/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email_same_activity(self, client, reset_activities, sample_email):
        """Test that signing up twice with same email returns error."""
        # Arrange
        activity_name = "Art Club"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_invalid_email_format(self, client, reset_activities):
        """Test signup with invalid email format."""
        # Act
        response = client.post(
            "/activities/Basketball Team/signup",
            params={"email": "invalid-email"}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_empty_email(self, client, reset_activities):
        """Test signup with empty email."""
        # Act
        response = client.post(
            "/activities/Basketball Team/signup",
            params={"email": ""}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_activity_with_spaces_in_name(self, client, reset_activities, sample_email):
        """Test signup for activity with spaces in name."""
        # Act
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
