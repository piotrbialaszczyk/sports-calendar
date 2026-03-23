from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app import api


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)


@app.get("/")
def root():
    return {"message": "Sports Calendar API"}