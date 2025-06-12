from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import create_access_token
from passlib.hash import bcrypt

login_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@login_router.post("/register")
def register(username: str = Form(...), password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, password=hashed_pw, role=role)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@login_router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
