"""
Endpoint tests for the Mergington High School Activities API.

Tests follow the Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and preconditions
- Act: Perform the action being tested
- Assert: Verify the results
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Verify response status is 200
        """
        # Arrange
        # (test client is provided by fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Verify response contains all expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Band",
            "Math Club",
            "Science Club",
        ]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_has_correct_structure(self, client):
        """
        Arrange: Initialize test client
        Act: Call GET /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(set(activity_data.keys()))
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """
        Arrange: Initialize test client with a new participant email
        Act: Sign up the participant for an activity
        Assert: Verify 200 status and correct response message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    def test_signup_adds_participant_to_activity(self, client):
        """
        Arrange: Initialize test client with a new participant email
        Act: Sign up the participant for an activity
        Assert: Verify participant is added to the activity's participant list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )
        response = client.get("/activities")

        # Assert
        activity_data = response.json()[activity_name]
        assert email in activity_data["participants"]

    def test_signup_fails_with_nonexistent_activity(self, client):
        """
        Arrange: Initialize test client with invalid activity name
        Act: Attempt to sign up for nonexistent activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_fails_when_already_signed_up(self, client):
        """
        Arrange: Initialize test client with an already-participating student
        Act: Attempt to sign up the same student again
        Assert: Verify 400 status and "Student already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club participants

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_successful(self, client):
        """
        Arrange: Initialize test client with an existing participant
        Act: Unregister the participant from an activity
        Assert: Verify 200 status and correct response message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister", params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"

    def test_unregister_removes_participant_from_activity(self, client):
        """
        Arrange: Initialize test client with an existing participant
        Act: Unregister the participant from an activity
        Assert: Verify participant is removed from the activity's participant list
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "sarah@mergington.edu"  # Already in participants

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister", params={"email": email}
        )
        response = client.get("/activities")

        # Assert
        activity_data = response.json()[activity_name]
        assert email not in activity_data["participants"]

    def test_unregister_fails_with_nonexistent_activity(self, client):
        """
        Arrange: Initialize test client with invalid activity name
        Act: Attempt to unregister from nonexistent activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_fails_when_participant_not_found(self, client):
        """
        Arrange: Initialize test client with valid activity but non-participant email
        Act: Attempt to unregister a student who is not in the activity
        Assert: Verify 404 status and "Participant not found" message
        """
        # Arrange
        activity_name = "Art Studio"
        email = "nonparticipant@mergington.edu"  # Not in Art Studio participants

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister", params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
