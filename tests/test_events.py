def test_create_event_valid(client):
    payload = {
        "date": "2024-01-01",
        "time": "12:00:00",
        "status": "played",
        "competition": {"name": "Test League"},
        "stage": {"name": "Final"},
        "home_team": {
            "official_name": "Team A",
            "abbreviation": "A",
            "country_code": "PL"
        },
        "away_team": {
            "official_name": "Team B",
            "abbreviation": "B",
            "country_code": "PL"
        },
        "result": {
            "home_goals": 2,
            "away_goals": 1
        }
    }

    response = client.post("/events", json=payload)

    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "played"
    assert data["home_team"]["official_name"] == "Team A"
    assert data["result"]["home_goals"] == 2

def test_create_event_played_without_result(client):
    payload = {
        "date": "2024-01-01",
        "time": "12:00:00",
        "status": "played",
        "competition": {"name": "Test League"},
        "stage": {"name": "Final"}
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422

def test_create_event_scheduled_with_result(client):
    payload = {
        "date": "2024-01-01",
        "time": "12:00:00",
        "status": "scheduled",
        "competition": {"name": "Test League"},
        "stage": {"name": "Final"},
        "result": {
            "home_goals": 1,
            "away_goals": 1
        }
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 422