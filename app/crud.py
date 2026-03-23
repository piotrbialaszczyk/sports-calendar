from sqlalchemy.orm import Session
from app.db.models import Team, Competition, Stage, Event, Result


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