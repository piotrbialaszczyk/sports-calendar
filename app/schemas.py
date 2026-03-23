from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional, Literal
from datetime import date, time


class TeamBase(BaseModel):
    official_name: str
    abbreviation: str
    country_code: str


class TeamResponse(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CompetitionBase(BaseModel):
    name: str


class CompetitionResponse(CompetitionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StageBase(BaseModel):
    name: str
    ordering: Optional[int] = None


class StageResponse(StageBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResultBase(BaseModel):
    home_goals: int
    away_goals: int
    winner: Optional[str] = None


class ResultResponse(ResultBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    date: date
    time: time
    status: Literal["scheduled", "played"]
    stadium: Optional[str] = None

    home_team: Optional[TeamBase] = None
    away_team: Optional[TeamBase] = None

    competition: CompetitionBase
    stage: StageBase

    result: Optional[ResultBase] = None

    @model_validator(mode="after")
    def validate_status_and_result(self):
        if self.status == "played" and self.result is None:
            raise ValueError("Played event must have result")

        if self.status == "scheduled" and self.result is not None:
            raise ValueError("Scheduled event cannot have result")

        return self


class EventResponse(BaseModel):
    id: int
    date: date
    time: time
    status: str
    stadium: Optional[str]

    home_team: Optional[TeamResponse]
    away_team: Optional[TeamResponse]

    competition: CompetitionResponse
    stage: StageResponse

    result: Optional[ResultResponse]

    model_config = ConfigDict(from_attributes=True)