from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.base import Base
from app.db.session import engine
from app import api


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)

app.mount("/", StaticFiles(directory="app/frontend", html=True), name="frontend")

@app.get("/")
def root():
    return {"message": "Sports Calendar API"}