from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship

from app.db.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    official_name = Column(String, unique=True, nullable=False)
    abbreviation = Column(String, nullable=False)
    country_code = Column(String, nullable=False)


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ordering = Column(Integer, nullable=True)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String, nullable=False)
    stadium = Column(String, nullable=True)

    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])

    competition = relationship("Competition")
    stage = relationship("Stage")

    result = relationship("Result", back_populates="event", uselist=False)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, ForeignKey("events.id"), unique=True, nullable=False)

    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
    winner = Column(String, nullable=True)

    event = relationship("Event", back_populates="result")