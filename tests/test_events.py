def create_event(client, payload):
    response = client.post("/events", json=payload)
    assert response.status_code == 200
    return response.json()

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

def test_get_events_returns_list(client):
    payload = {
        "date": "2024-01-01",
        "time": "10:00:00",
        "status": "played",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"},
        "result": {"home_goals": 1, "away_goals": 0}
    }

    create_event(client, payload)

    response = client.get("/events")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

def test_get_events_filter_by_status(client):
    payload1 = {
        "date": "2024-01-01",
        "time": "10:00:00",
        "status": "played",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"},
        "result": {"home_goals": 1, "away_goals": 0}
    }

    payload2 = {
        "date": "2024-01-02",
        "time": "11:00:00",
        "status": "scheduled",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"}
    }

    create_event(client, payload1)
    create_event(client, payload2)

    response = client.get("/events?status=played")

    data = response.json()

    assert len(data) == 1
    assert data[0]["status"] == "played"

def test_get_events_sort_by_date(client):
    payload1 = {
        "date": "2024-01-02",
        "time": "10:00:00",
        "status": "played",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"},
        "result": {"home_goals": 1, "away_goals": 0}
    }

    payload2 = {
        "date": "2024-01-01",
        "time": "10:00:00",
        "status": "played",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"},
        "result": {"home_goals": 1, "away_goals": 0}
    }

    create_event(client, payload1)
    create_event(client, payload2)

    response = client.get("/events?sort=date")

    data = response.json()

    assert data[0]["date"] == "2024-01-01"

def test_get_events_invalid_sort(client):
    response = client.get("/events?sort=invalid")

    assert response.status_code == 400

def test_get_events_pagination(client):
    for i in range(5):
        payload = {
            "date": f"2024-01-0{i+1}",
            "time": "10:00:00",
            "status": "played",
            "competition": {"name": "League"},
            "stage": {"name": "Stage"},
            "result": {"home_goals": 1, "away_goals": 0}
        }
        create_event(client, payload)

    response = client.get("/events?limit=2&offset=0")
    data = response.json()

    assert len(data) == 2

def test_get_event_by_id_success(client):
    payload = {
        "date": "2024-01-01",
        "time": "10:00:00",
        "status": "played",
        "competition": {"name": "League"},
        "stage": {"name": "Stage"},
        "result": {"home_goals": 1, "away_goals": 0}
    }

    event = create_event(client, payload)

    response = client.get(f"/events/{event['id']}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == event["id"]
    assert data["status"] == "played"

def test_get_event_by_id_not_found(client):
    response = client.get("/events/999")

    assert response.status_code == 404