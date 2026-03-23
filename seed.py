import json

from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.db.models import Result, Event, Team, Competition, Stage
from app import crud
from app.schemas import EventCreate


Base.metadata.create_all(bind=engine)


def parse_team(team_data):
    if not team_data:
        return None

    return {
        "official_name": team_data.get("officialName"),
        "abbreviation": team_data.get("abbreviation"),
        "country_code": team_data.get("teamCountryCode"),
    }


def parse_result(result_data):
    if not result_data:
        return None

    return {
        "home_goals": result_data.get("homeGoals"),
        "away_goals": result_data.get("awayGoals"),
        "winner": result_data.get("winner"),
    }


def main():
    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:
        # reset database (deterministic seed)
        db.query(Result).delete()
        db.query(Event).delete()
        db.query(Team).delete()
        db.query(Competition).delete()
        db.query(Stage).delete()
        db.commit()

        with open("sample.json") as f:
            data = json.load(f)["data"]

        for item in data:
            event_data = {
                "date": item["dateVenue"],
                "time": item["timeVenueUTC"],
                "status": item["status"],
                "stadium": item.get("stadium"),
                "home_team": parse_team(item.get("homeTeam")),
                "away_team": parse_team(item.get("awayTeam")),
                "competition": {
                    "name": item.get("originCompetitionName") or "Unknown Competition"
                },
                "stage": {
                    "name": item["stage"]["name"],
                    "ordering": item["stage"].get("ordering"),
                },
                "result": parse_result(item.get("result")),
            }

            if event_data["status"] == "scheduled":
                event_data["result"] = None

            if event_data["status"] == "played" and not event_data["result"]:
                print(f"Skipping invalid event: {item}")
                skipped += 1
                continue

            event_schema = EventCreate(**event_data)

            home_team = crud.get_or_create_team(db, event_schema.home_team)
            away_team = crud.get_or_create_team(db, event_schema.away_team)

            existing_event = db.query(Event).filter_by(
                date=event_schema.date,
                time=event_schema.time,
                home_team_id=home_team.id if home_team else None,
                away_team_id=away_team.id if away_team else None,
            ).first()

            if existing_event:
                skipped += 1
                continue

            crud.create_event(db, event_schema)
            inserted += 1

        db.commit()
        print(f"Inserted: {inserted}, Skipped: {skipped}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()