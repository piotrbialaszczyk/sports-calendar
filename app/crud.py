from sqlalchemy.orm import Session
from app.db.models import Team, Competition, Stage, Event, Result
from sqlalchemy.orm import joinedload


ALLOWED_SORT_FIELDS = {"date", "time", "status"}

def get_or_create_team(db: Session, team_data):
    if team_data is None:
        return None

    team = db.query(Team).filter_by(official_name=team_data.official_name).first()
    if team:
        return team

    team = Team(
        official_name=team_data.official_name,
        abbreviation=team_data.abbreviation,
        country_code=team_data.country_code,
    )
    db.add(team)
    db.flush()
    return team


def get_or_create_competition(db: Session, comp_data):
    comp = db.query(Competition).filter_by(name=comp_data.name).first()
    if comp:
        return comp

    comp = Competition(name=comp_data.name)
    db.add(comp)
    db.flush()
    return comp


def get_or_create_stage(db: Session, stage_data):
    stage = db.query(Stage).filter_by(name=stage_data.name).first()
    if stage:
        return stage

    stage = Stage(name=stage_data.name, ordering=stage_data.ordering)
    db.add(stage)
    db.flush()
    return stage


def create_event(db: Session, event):
    home_team = get_or_create_team(db, event.home_team)
    away_team = get_or_create_team(db, event.away_team)

    competition = get_or_create_competition(db, event.competition)
    stage = get_or_create_stage(db, event.stage)

    db_event = Event(
        date=event.date,
        time=event.time,
        status=event.status,
        stadium=event.stadium,
        home_team_id=home_team.id if home_team else None,
        away_team_id=away_team.id if away_team else None,
        competition_id=competition.id,
        stage_id=stage.id,
    )

    db.add(db_event)
    db.flush()

    if event.result:
        db_result = Result(
            event_id=db_event.id,
            home_goals=event.result.home_goals,
            away_goals=event.result.away_goals,
            winner=event.result.winner,
        )
        db.add(db_result)

    return db_event

def get_events(db, date=None, status=None, sort=None, limit=10, offset=0):
    query = db.query(Event).options(
        joinedload(Event.home_team),
        joinedload(Event.away_team),
        joinedload(Event.competition),
        joinedload(Event.stage),
        joinedload(Event.result),
    )

    if date:
        query = query.filter(Event.date == date)

    if status:
        query = query.filter(Event.status == status)

    if sort:
        direction = "asc"
        field_name = sort

        if sort.startswith("-"):
            direction = "desc"
            field_name = sort[1:]

        if field_name not in ALLOWED_SORT_FIELDS:
            raise ValueError(f"Invalid sort field: {field_name}")

        column = getattr(Event, field_name)

        if direction == "desc":
            column = column.desc()

        query = query.order_by(column)

    query = query.offset(offset).limit(limit)

    return query.all()

def get_event_by_id(db, event_id):
    return (
        db.query(Event)
        .options(
            joinedload(Event.home_team),
            joinedload(Event.away_team),
            joinedload(Event.competition),
            joinedload(Event.stage),
            joinedload(Event.result),
        )
        .filter(Event.id == event_id)
        .first()
    )