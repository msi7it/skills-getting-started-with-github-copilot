def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_data(client):
    # Arrange

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_new_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data == {"message": f"Signed up {email} for {activity}"}

    refreshed = client.get("/activities").json()
    assert email in refreshed[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up"


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data == {"message": f"Removed {email} from {activity}"}

    refreshed = client.get("/activities").json()
    assert email not in refreshed[activity]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"
