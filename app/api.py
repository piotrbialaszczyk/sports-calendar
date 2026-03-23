from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import SessionLocal
from app.db.models import Event
from app.schemas import EventCreate, EventResponse
from app import crud

from typing import Optional
from datetime import date

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
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

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/events", response_model=list[EventResponse])
def get_events_endpoint(
    date: Optional[date] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    try:
        events = crud.get_events(
            db,
            date=date,
            status=status,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        return events
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event