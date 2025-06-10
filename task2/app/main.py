from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    return auth.register_user(user, db)

@app.post("/login", response_model=schemas.UserResponse)
def login(user: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    return auth.login_user(user, db)
