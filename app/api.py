from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.session import SessionLocal
from app.db.models import Event
from app.schemas import EventCreate, EventResponse
from app import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events", response_model=EventResponse)
def create_event_endpoint(event: EventCreate, db: Session = Depends(get_db)):
    try:
        db_event = crud.create_event(db, event)

        db.commit()
        db.refresh(db_event)

        db_event = (
            db.query(Event)
            .options(
                joinedload(Event.home_team),
                joinedload(Event.away_team),
                joinedload(Event.competition),
                joinedload(Event.stage),
                joinedload(Event.result),
            )
            .filter(Event.id == db_event.id)
            .first()
        )

        return db_event

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))