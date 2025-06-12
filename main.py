from fastapi import FastAPI
from login import login_router
from models import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(login_router)
