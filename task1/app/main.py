from fastapi import FastAPI
from .database import init_db
from .models import Note

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Task 1!"}
