# Sports Event Calendar

## Overview

This project is a full-stack application for managing and displaying sports events.

It includes:

* a normalized relational database
* a FastAPI backend
* a simple frontend (HTML + JavaScript)
* automated tests using pytest
* a seed script to populate the database from JSON data

The application allows users to:

* create events with teams, results, competition, and stage
* retrieve and filter events via API
* view events in both table and calendar formats

---

## Tech Stack

* **Backend:** FastAPI, SQLAlchemy
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript (no frameworks)
* **Testing:** pytest
* **Data:** JSON seed file

---

## Project Structure

```
app/
├── api.py
├── crud.py
├── schemas.py
├── db/
│   ├── models.py
│   ├── session.py
│   └── base.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js

tests/
├── conftest.py
├── test_events.py

main.py
seed.py
sample.json
requirements.txt
```

---

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### 1. Seed the database

```bash
python seed.py
```

This will:

* reset the database
* load data from `data/sample.json`
* normalize inconsistent input data
* prevent duplicates

---

### 2. Start the server

```bash
uvicorn main:app --reload
```

---

### 3. Open in browser

```
http://127.0.0.1:8000
```

The frontend is served directly by FastAPI.

---

## API Endpoints

### POST /events

Create a new event.

Rules:

* `played` events must include a result
* `scheduled` events cannot include a result
* teams are deduplicated before insertion
* all operations are executed in a single transaction

---

### GET /events

Returns a list of events.

Supports:

* filtering: `?status=played`
* sorting: `?sort=date`, `?sort=-date`
* pagination: `?limit=10&offset=0`

---

### GET /events/{id}

Returns a single event by ID.

* returns 404 if not found

---

## Database Design

The database follows normalization principles (3NF).

### Main entities:

* Event
* Team
* Result
* Competition
* Stage

### Relationships:

* Event → Team (home and away)
* Event → Competition
* Event → Stage
* Event → Result (1:1)

Additional fields:

* stadium (event)
* team metadata (official_name, abbreviation, country_code)

An ERD diagram is included in the repository.

---

## Testing

Run tests with:

```bash
pytest -v
```

Tests cover:

* valid event creation
* validation rules (played vs scheduled)
* filtering, sorting, pagination
* retrieving single events
* 404 handling

An in-memory SQLite database is used for isolation.

---

## Frontend

The frontend is intentionally simple and framework-free.

### Table View

* displays all events
* formatted team information
* highlights played events

### Calendar View

* monthly layout (Monday start)
* correct date alignment
* events grouped per day
* events sorted by time
* navigation between months

A simple navigation bar allows switching between sections.

---

## Data Handling

The seed script:

* handles missing teams and results
* normalizes inconsistent data
* skips invalid records
* prevents duplicates
* uses a single transaction
* resets the database for deterministic results

---

## Naming Conventions

Foreign keys are named using the pattern `<entity>_id` (e.g. `home_team_id`, `competition_id`).

Although the task description suggested prefixing foreign keys with an underscore, this convention was chosen because it is more descriptive and aligns with common industry practices.

---

## Notes

* The solution prioritizes clarity, correctness, and maintainability
* No frontend frameworks were used to keep the implementation transparent
* Backend logic is separated into schemas, CRUD, and API layers
* Create a .env file based on .env.example before running the application.
