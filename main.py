from app.db.base import Base
from app.db.session import engine
from app.db import models

Base.metadata.create_all(bind=engine)

print("Tables created")