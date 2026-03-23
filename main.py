from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.db import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Sports Calendar API"}